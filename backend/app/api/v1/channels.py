from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, and_, or_, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import IntegrityError
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
from app.models.channel_join_request import ChannelJoinRequest
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
    MessageEditRequest,
    CoverUploadResponse,
    JoinRequestCreate,
    JoinRequestResponse,
    JoinRequestListResponse,
    JoinRequestReview,
    JoinChannelResponse,
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
        # 如果频道没有封面，使用作品封面作为 fallback
        if not data["cover_image"] and work.cover_image:
            data["cover_image"] = work.cover_image

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
    # 获取所有频道成员（除了发送者和被封禁的用户）
    members_result = await db.execute(
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id != sender_id,
            ChannelMember.is_banned == False  # 过滤被封禁用户
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


# ===== 频道封面上传 =====
from fastapi import UploadFile, File as FastAPIFile
from app.services.cos_service import get_cos_service as get_cos_service_for_cover

@router.post("/upload-cover", response_model=CoverUploadResponse)
async def upload_channel_cover(
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_active_user),
):
    """
    上传频道封面图片
    返回图片 URL，在创建频道时使用
    """
    # 验证文件类型
    allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅支持 JPG、PNG、WebP、GIF 格式的图片"
        )

    # 读取文件内容
    content = await file.read()

    # 验证文件大小 (最大 5MB)
    max_size = 5 * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="图片大小不能超过 5MB"
        )

    # 上传到 COS
    try:
        cos_service = get_cos_service_for_cover()
        cover_url = await cos_service.upload_channel_cover(
            filename=file.filename,
            content=content,
            content_type=file.content_type
        )
    except Exception as e:
        logger.error(f"上传频道封面失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="上传失败，请稍后重试"
        )

    return CoverUploadResponse(cover_url=cover_url)


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

    # 查询当前用户在所有频道中的成员关系（包含被封禁状态，用于判断）
    channel_ids = [c.id for c in all_channels]
    if channel_ids:  # 只有在有频道时才查询
        members_query = select(ChannelMember).where(
            ChannelMember.channel_id.in_(channel_ids),
            ChannelMember.user_id == current_user.id
            # 不过滤 is_banned，需要知道封禁状态
        )
        members_result = await db.execute(members_query)
        members = {m.channel_id: m for m in members_result.scalars().all()}
    else:
        members = {}

    # 构建响应
    channel_responses = []
    for channel in all_channels:
        member = members.get(channel.id)

        # 被封禁的非官方频道不显示在列表中
        if member and member.is_banned and channel.type != 'official':
            continue

        channel_data = build_channel_response(channel, channel.work)
        # 添加当前用户在该频道中的角色
        if member:
            if member.is_banned:
                # 被封禁用户：角色为 None，标记无法访问
                channel_data['current_user_role'] = None
                channel_data['can_access'] = False
            else:
                channel_data['current_user_role'] = member.role
                # 检查用户是否满足进入要求
                can_access = await check_channel_access(channel, current_user, db)
                channel_data['can_access'] = can_access
        elif channel.type == 'official':
            # 官方频道默认为member角色（如果用户是管理员，会在自动加入时设置为owner）
            channel_data['current_user_role'] = 'owner' if current_user.is_admin else 'member'
            channel_data['can_access'] = True
        else:
            channel_data['current_user_role'] = None
            channel_data['can_access'] = False

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


@router.post("/join", response_model=JoinChannelResponse)
async def join_channel(
    data: JoinRequestCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    加入频道
    - 官方频道：直接加入
    - 其他频道（私域/作品）：创建加入申请，等待审核
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
    member = existing_member.scalar_one_or_none()
    if member:
        if member.is_banned:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您已被移出该频道，无法重新加入"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经是频道成员"
        )

    # 官方频道：直接加入
    if channel.type == 'official':
        member_role = 'owner' if current_user.is_admin else 'member'
        member = ChannelMember(
            id=uuid.uuid4(),
            channel_id=data.channel_id,
            user_id=current_user.id,
            role=member_role
        )
        db.add(member)
        channel.member_count += 1
        await db.commit()
        await db.refresh(member)

        return JoinChannelResponse(
            status="joined",
            message="已成功加入频道",
            member=ChannelMemberResponse(
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
        )

    # 作品频道：检查用户是否已收藏该作品，如果是则直接加入
    if channel.type == 'work' and channel.work_id:
        from app.models.bookshelf import Bookshelf
        bookshelf_result = await db.execute(
            select(Bookshelf).where(
                Bookshelf.user_id == current_user.id,
                Bookshelf.work_id == channel.work_id
            )
        )
        if bookshelf_result.scalar_one_or_none():
            # 用户已收藏该作品，直接加入频道
            member = ChannelMember(
                id=uuid.uuid4(),
                channel_id=data.channel_id,
                user_id=current_user.id,
                role='member'
            )
            db.add(member)
            channel.member_count += 1
            await db.commit()
            await db.refresh(member)

            return JoinChannelResponse(
                status="joined",
                message="已成功加入书友圈",
                member=ChannelMemberResponse(
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
            )

    # 非官方频道：创建加入申请
    # 检查是否已有待审核的申请
    existing_request = await db.execute(
        select(ChannelJoinRequest).where(
            ChannelJoinRequest.channel_id == data.channel_id,
            ChannelJoinRequest.user_id == current_user.id,
            ChannelJoinRequest.status == 'pending'
        )
    )
    if existing_request.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已有待审核的加入申请"
        )

    # 创建申请
    join_request = ChannelJoinRequest(
        id=uuid.uuid4(),
        channel_id=data.channel_id,
        user_id=current_user.id,
        message=data.message,
        status='pending'
    )
    db.add(join_request)
    await db.commit()
    await db.refresh(join_request)

    return JoinChannelResponse(
        status="pending",
        message="申请已提交，请等待管理员审核",
        request_id=join_request.id
    )


@router.get("/my-join-requests", response_model=JoinRequestListResponse)
async def get_my_join_requests(
    status_filter: Optional[str] = Query(None, description="过滤状态: pending, approved, rejected"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取我的加入申请列表
    """
    query = select(ChannelJoinRequest).where(
        ChannelJoinRequest.user_id == current_user.id
    )

    if status_filter:
        query = query.where(ChannelJoinRequest.status == status_filter)

    query = query.order_by(ChannelJoinRequest.created_at.desc())

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    requests = result.scalars().all()

    response_requests = []
    for req in requests:
        response_requests.append(JoinRequestResponse(
            id=req.id,
            channel_id=req.channel_id,
            user_id=req.user_id,
            message=req.message,
            status=req.status,
            reviewed_by=req.reviewed_by,
            reviewed_at=req.reviewed_at,
            reject_reason=req.reject_reason,
            created_at=req.created_at,
            user_name=current_user.username,
            user_avatar=current_user.avatar
        ))

    return JoinRequestListResponse(requests=response_requests, total=total)


@router.get("/{channel_id}/join-requests", response_model=JoinRequestListResponse)
async def get_join_requests(
    channel_id: UUID,
    status_filter: Optional[str] = Query(None, description="过滤状态: pending, approved, rejected"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取频道加入申请列表（管理员/owner）
    """
    # 检查权限
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()

    if not member or member.role not in ['owner', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看加入申请"
        )

    # 构建查询
    query = select(ChannelJoinRequest).where(
        ChannelJoinRequest.channel_id == channel_id
    )

    if status_filter:
        query = query.where(ChannelJoinRequest.status == status_filter)

    # 排序：待审核优先，然后按时间倒序
    query = query.order_by(
        case(
            (ChannelJoinRequest.status == 'pending', 0),
            else_=1
        ),
        ChannelJoinRequest.created_at.desc()
    )

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    requests = result.scalars().all()

    # 获取用户信息
    user_ids = [r.user_id for r in requests]
    reviewer_ids = [r.reviewed_by for r in requests if r.reviewed_by]
    all_user_ids = list(set(user_ids + reviewer_ids))

    users_map = {}
    if all_user_ids:
        users_result = await db.execute(
            select(User).where(User.id.in_(all_user_ids))
        )
        for user in users_result.scalars().all():
            users_map[user.id] = user

    # 构建响应
    response_requests = []
    for req in requests:
        user = users_map.get(req.user_id)
        reviewer = users_map.get(req.reviewed_by) if req.reviewed_by else None
        response_requests.append(JoinRequestResponse(
            id=req.id,
            channel_id=req.channel_id,
            user_id=req.user_id,
            message=req.message,
            status=req.status,
            reviewed_by=req.reviewed_by,
            reviewed_at=req.reviewed_at,
            reject_reason=req.reject_reason,
            created_at=req.created_at,
            user_name=user.username if user else None,
            user_avatar=user.avatar if user else None,
            reviewer_name=reviewer.username if reviewer else None
        ))

    return JoinRequestListResponse(requests=response_requests, total=total)


@router.post("/{channel_id}/join-requests/{request_id}/review")
async def review_join_request(
    channel_id: UUID,
    request_id: UUID,
    data: JoinRequestReview,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    审核加入申请
    """
    from datetime import datetime, timezone

    # 检查权限
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()

    if not member or member.role not in ['owner', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以审核申请"
        )

    # 获取申请
    request_result = await db.execute(
        select(ChannelJoinRequest).where(
            ChannelJoinRequest.id == request_id,
            ChannelJoinRequest.channel_id == channel_id
        )
    )
    join_request = request_result.scalar_one_or_none()

    if not join_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="申请不存在"
        )

    if join_request.status != 'pending':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该申请已被处理"
        )

    # 获取频道
    channel_result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = channel_result.scalar_one_or_none()

    # 处理申请
    if data.action == 'approve':
        # 检查申请人是否已经是成员或被封禁
        existing_member = await db.execute(
            select(ChannelMember).where(
                ChannelMember.channel_id == channel_id,
                ChannelMember.user_id == join_request.user_id
            )
        )
        existing = existing_member.scalar_one_or_none()

        if existing:
            if existing.is_banned:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该用户已被封禁，无法通过申请"
                )
            # 已经是成员，直接标记申请为通过
            join_request.status = 'approved'
            join_request.reviewed_by = current_user.id
            join_request.reviewed_at = datetime.now(timezone.utc)
            await db.commit()
            return {"message": "用户已是成员，申请已标记为通过", "status": "approved"}

        # 通过申请：创建成员记录
        new_member = ChannelMember(
            id=uuid.uuid4(),
            channel_id=channel_id,
            user_id=join_request.user_id,
            role='member'
        )
        db.add(new_member)
        channel.member_count += 1

        join_request.status = 'approved'
        join_request.reviewed_by = current_user.id
        join_request.reviewed_at = datetime.now(timezone.utc)

        await db.commit()
        return {"message": "已通过申请", "status": "approved"}

    else:  # reject
        join_request.status = 'rejected'
        join_request.reviewed_by = current_user.id
        join_request.reviewed_at = datetime.now(timezone.utc)
        join_request.reject_reason = data.reject_reason

        await db.commit()
        return {"message": "已拒绝申请", "status": "rejected"}


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

    # 被封禁用户不能主动退出
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已被封禁，无法退出频道"
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

    # 获取所有成员（排除被封禁的）
    result = await db.execute(
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.is_banned == False  # 过滤被封禁用户
        )
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
                "full_name": member.user.full_name if member.user else None,
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
    踢出频道成员（owner 和 admin 可操作）
    - owner 可以踢出 admin 和 member
    - admin 只能踢出 member
    """
    # 检查当前用户权限
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

    if current_member.role not in ['owner', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以踢出成员"
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

    # 不能踢出 owner
    if target_member.role == 'owner':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能踢出频道创建者"
        )

    # admin 不能踢出其他 admin
    if current_member.role == 'admin' and target_member.role == 'admin':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="管理员不能踢出其他管理员"
        )

    channel = current_member.channel

    # 官方频道：设置封禁标记而不是删除（防止用户自动重新加入）
    if channel.type == "official":
        from datetime import datetime, timezone
        target_member.is_banned = True
        target_member.banned_at = datetime.now(timezone.utc)  # 记录封禁时间
        target_member.role = "member"  # 降级为普通成员
    else:
        # 其他频道：删除成员记录
        await db.delete(target_member)
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

    # 检查是否是频道成员
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()

    # 如果不是成员
    if not member:
        # 官方频道：自动加入
        if channel.type == "official":
            # 先检查是否存在被封禁的记录（防止"复活"）
            banned_check = await db.execute(
                select(ChannelMember).where(
                    ChannelMember.channel_id == channel_id,
                    ChannelMember.user_id == current_user.id,
                    ChannelMember.is_banned == True
                )
            )
            banned_member = banned_check.scalar_one_or_none()
            if banned_member:
                # 被封禁用户不能自动加入，但可以查看封禁前的消息
                member = banned_member
            else:
                member_role = "owner" if current_user.is_admin else "member"
                try:
                    member = ChannelMember(
                        id=uuid.uuid4(),
                        channel_id=channel_id,
                        user_id=current_user.id,
                        role=member_role,
                        joined_at=func.now()
                    )
                    db.add(member)
                    channel.member_count += 1
                    await db.flush()
                except IntegrityError:
                    # 竞态条件：其他请求已创建成员记录，回滚后重新查询
                    await db.rollback()
                    member_result = await db.execute(
                        select(ChannelMember).where(
                            ChannelMember.channel_id == channel_id,
                            ChannelMember.user_id == current_user.id
                        )
                    )
                    member = member_result.scalar_one_or_none()
                    if not member:
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="加入频道失败"
                        )
                    # 如果是被封禁的用户，后面会限制消息可见范围
        else:
            # 非官方频道：必须先加入
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="未加入该频道"
            )

    # 注意：被封禁用户仍可查看消息，但只能看到封禁前的消息（下面的查询会限制）

    # 查询消息
    query = (
        select(ChannelMessage)
        .where(
            ChannelMessage.channel_id == channel_id,
            ChannelMessage.is_deleted == False
        )
        .options(
            selectinload(ChannelMessage.user),
            selectinload(ChannelMessage.attachments),
            selectinload(ChannelMessage.forwarded_from).selectinload(ChannelMessage.user),
            selectinload(ChannelMessage.forwarded_from).selectinload(ChannelMessage.channel),
            selectinload(ChannelMessage.forwarded_from).selectinload(ChannelMessage.attachments)
        )
        .order_by(ChannelMessage.created_at.asc())
    )

    # 如果用户被封禁，只能看到封禁前的消息
    banned_at_filter = None
    if member.is_banned and member.banned_at:
        banned_at_filter = member.banned_at
        query = query.where(ChannelMessage.created_at <= member.banned_at)

    # 获取总数
    count_query = select(func.count(ChannelMessage.id)).where(
        ChannelMessage.channel_id == channel_id,
        ChannelMessage.is_deleted == False
    )
    # 封禁用户的总数也要限制
    if banned_at_filter:
        count_query = count_query.where(ChannelMessage.created_at <= banned_at_filter)
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
        # 构建附件列表
        attachments_data = [
            {
                "id": att.id,
                "file_name": att.file_name,
                "file_type": att.file_type,
                "file_size": att.file_size,
                "file_url": att.file_url,
                "thumbnail_url": att.thumbnail_url,
                "created_at": att.created_at
            }
            for att in (msg.attachments or [])
        ]

        # 构建转发来源信息
        forwarded_from_data = None
        if msg.forwarded_from_id and msg.forwarded_from:
            orig = msg.forwarded_from
            orig_attachments = [
                {
                    "id": str(att.id),
                    "file_name": att.file_name,
                    "file_type": att.file_type,
                    "file_url": att.file_url,
                    "thumbnail_url": att.thumbnail_url
                }
                for att in (orig.attachments or [])
            ]
            forwarded_from_data = {
                "message_id": str(orig.id),
                "channel_id": str(orig.channel_id),
                "channel_name": orig.channel.name if orig.channel else "已删除频道",
                "user_id": str(orig.user_id) if orig.user_id else None,
                "user_name": orig.user.username if orig.user else "已删除用户",
                "user_avatar": orig.user.avatar if orig.user else None,
                "user_bio": orig.user.bio if orig.user else None,
                "user_honor": orig.user.honor if orig.user else None,
                "content": orig.content,
                "created_at": orig.created_at.isoformat() if orig.created_at else None,
                "attachments": orig_attachments
            }

        message_responses.append(ChannelMessageResponse(
            id=msg.id,
            channel_id=msg.channel_id,
            user_id=msg.user_id,
            content=msg.content,
            type=msg.type,
            is_pinned=msg.is_pinned,
            is_deleted=msg.is_deleted,
            is_edited=msg.is_edited,
            reply_to_id=msg.reply_to_id,
            forwarded_from_id=msg.forwarded_from_id,
            forwarded_from=forwarded_from_data,
            reaction_count=msg.reaction_count,
            created_at=msg.created_at,
            updated_at=msg.updated_at,
            deleted_at=msg.deleted_at,
            edited_at=msg.edited_at,
            user_name=msg.user.username if msg.user else "已删除用户",
            user_avatar=msg.user.avatar if msg.user else None,
            user_bio=msg.user.bio if msg.user else None,
            user_honor=msg.user.honor if msg.user else None,
            user_title=member.custom_title if member else None,
            user_title_color=member.title_color if member else None,
            attachments=attachments_data
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

    # 检查频道是否已锁定
    if channel.status == "locked":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="频道已锁定，无法发送消息"
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
            # 先检查是否存在被封禁的记录（防止"复活"）
            banned_check = await db.execute(
                select(ChannelMember).where(
                    ChannelMember.channel_id == channel_id,
                    ChannelMember.user_id == current_user.id,
                    ChannelMember.is_banned == True
                )
            )
            if banned_check.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="您已被移出该频道，无法发送消息"
                )

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

    # 检查是否被封禁（官方频道踢出后的用户）
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法发送消息"
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

    # 检查慢速模式
    if channel.slowmode_interval and channel.slowmode_interval > 0:
        # 管理员和群主不受慢速模式限制
        if member.role not in ['owner', 'admin']:
            # 获取用户最后一条消息的时间
            last_msg_result = await db.execute(
                select(ChannelMessage.created_at)
                .where(
                    ChannelMessage.channel_id == channel_id,
                    ChannelMessage.user_id == current_user.id,
                    ChannelMessage.is_deleted == False
                )
                .order_by(ChannelMessage.created_at.desc())
                .limit(1)
            )
            last_msg_time = last_msg_result.scalar_one_or_none()

            if last_msg_time:
                from datetime import datetime, timezone, timedelta
                time_since_last = datetime.now(timezone.utc) - last_msg_time
                if time_since_last.total_seconds() < channel.slowmode_interval:
                    remaining = channel.slowmode_interval - int(time_since_last.total_seconds())
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"慢速模式已启用，请等待 {remaining} 秒后再发送消息"
                    )

    # 只有粉丝群、官方频道、作品群的创建者可以发送公告
    if message_type == "announcement":
        if (channel.type not in ['fangroup', 'official', 'work']) or member.role != 'owner':
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

    # WebSocket 广播新消息
    from app.api.v1.ws import broadcast_channel_message
    await broadcast_channel_message(channel_id, {
        "id": str(message.id),
        "channel_id": str(message.channel_id),
        "user_id": str(message.user_id),
        "content": message.content,
        "type": message.type,
        "is_pinned": message.is_pinned,
        "reply_to_id": str(message.reply_to_id) if message.reply_to_id else None,
        "forwarded_from_id": None,
        "reaction_count": message.reaction_count,
        "created_at": message.created_at.isoformat(),
        "user_name": current_user.username,
        "user_avatar": current_user.avatar,
        "user_bio": current_user.bio,
        "user_honor": current_user.honor,
        "user_title": member.custom_title,
        "user_title_color": member.title_color,
        "attachments": []
    }, exclude_user=current_user.id)

    return ChannelMessageResponse(
        id=message.id,
        channel_id=message.channel_id,
        user_id=message.user_id,
        content=message.content,
        type=message.type,
        is_pinned=message.is_pinned,
        is_deleted=message.is_deleted,
        is_edited=message.is_edited,
        reply_to_id=message.reply_to_id,
        reaction_count=message.reaction_count,
        created_at=message.created_at,
        updated_at=message.updated_at,
        deleted_at=message.deleted_at,
        user_name=current_user.username,
        user_avatar=current_user.avatar,
        user_bio=current_user.bio,
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
    member = member_check.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该频道的成员"
        )

    # 检查是否被封禁
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道"
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
    更新频道信息（仅创建者可操作，支持粉丝群和作品频道）
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

    # 检查是否为粉丝群或作品频道
    if channel.type not in ("fangroup", "work"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能更新粉丝群或作品频道"
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
    member = member_check.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 检查是否被封禁
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道"
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
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 构建查询条件
    conditions = [
        ChannelMessage.channel_id == channel_id,
        ChannelMessage.type == "announcement",
        ChannelMessage.is_deleted == False
    ]

    # 如果用户被封禁，只能看到封禁前的公告
    if member.is_banned and member.banned_at:
        conditions.append(ChannelMessage.created_at <= member.banned_at)

    # 获取所有公告消息
    announcements_result = await db.execute(
        select(ChannelMessage)
        .where(*conditions)
        .options(
            selectinload(ChannelMessage.user),
            selectinload(ChannelMessage.attachments)
        )
        .order_by(ChannelMessage.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    announcements = announcements_result.scalars().all()

    # 获取总数
    total_result = await db.execute(
        select(func.count(ChannelMessage.id)).where(*conditions)
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
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 构建查询条件
    conditions = [
        ChannelMessage.channel_id == channel_id,
        ChannelMessage.type == "announcement",
        ChannelMessage.is_deleted == False
    ]

    # 如果用户被封禁，只能看到封禁前的公告
    if member.is_banned and member.banned_at:
        conditions.append(ChannelMessage.created_at <= member.banned_at)

    # 获取最新公告
    latest_result = await db.execute(
        select(ChannelMessage)
        .where(*conditions)
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
    - 创建者/管理员：可以撤回所有人的消息，无时间限制
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

    # 检查是否是管理员
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    is_admin = member and member.role in ['owner', 'admin']

    # 检查是否被封禁
    if member and member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法撤回消息"
        )

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

    # 如果不是创建者或管理员,检查是否是消息发送者
    if not is_creator and not is_admin:
        if message.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只能撤回自己的消息"
            )

    # 标记为已删除
    message.is_deleted = True
    message.deleted_at = func.now()
    message.content = "[此消息已被撤回]"

    await db.commit()

    # WebSocket 广播消息撤回
    from app.api.v1.ws import broadcast_message_delete
    await broadcast_message_delete(channel_id, str(message_id))

    return {"message": "消息已撤回"}


@router.patch("/{channel_id}/messages/{message_id}")
async def edit_message(
    channel_id: UUID,
    message_id: UUID,
    request: MessageEditRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    编辑消息
    - 只能编辑自己发送的消息
    - 只能在发送后10分钟内编辑
    - 编辑后会标记为"已编辑"
    """
    from datetime import datetime, timedelta, timezone

    content = request.content

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
            detail="消息已被删除，无法编辑"
        )

    # 检查是否是消息发送者
    if message.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能编辑自己的消息"
        )

    # 检查是否被封禁
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()

    if member and member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法编辑消息"
        )

    # 检查是否超过10分钟
    time_limit = timedelta(minutes=10)
    now = datetime.now(timezone.utc)

    if message.created_at.tzinfo is None:
        created_at = message.created_at.replace(tzinfo=timezone.utc)
    else:
        created_at = message.created_at

    if now - created_at > time_limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="超过编辑时限（10分钟）"
        )

    # 更新消息内容
    message.content = content
    message.is_edited = True
    message.edited_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(message)

    # WebSocket 广播消息编辑
    from app.api.v1.ws import broadcast_message_edit
    await broadcast_message_edit(
        channel_id,
        str(message_id),
        content,
        str(current_user.id),
        current_user.username,
        message.edited_at.isoformat() if message.edited_at else None
    )

    return {
        "id": str(message.id),
        "channelId": str(message.channel_id),
        "userId": str(message.user_id) if message.user_id else None,
        "userName": current_user.username,
        "userAvatar": current_user.avatar,
        "userTitle": member.custom_title if member else None,
        "userTitleColor": member.title_color if member else None,
        "content": message.content,
        "type": message.type,
        "isPinned": message.is_pinned,
        "isDeleted": message.is_deleted,
        "isEdited": message.is_edited,
        "replyToId": str(message.reply_to_id) if message.reply_to_id else None,
        "reactionCount": message.reaction_count,
        "createdAt": message.created_at.isoformat(),
        "updatedAt": message.updated_at.isoformat(),
        "editedAt": message.edited_at.isoformat() if message.edited_at else None
    }


# ===== 搜索功能 API =====

@router.get("/{channel_id}/search")
async def search_messages(
    channel_id: UUID,
    keyword: Optional[str] = Query(None, min_length=1, description="搜索关键词"),
    content_type: Optional[str] = Query(
        None,
        regex="^(image_video|file|link)$",
        description="内容类型: image_video/file/link"
    ),
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
    支持按关键词、内容类型、发送者、日期范围筛选
    content_type: image_video(图片和视频) | file(文件) | link(链接)
    """
    # 检查是否是频道成员
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 注意：允许不传任何筛选条件，此时返回所有消息（用于"全部"标签）

    # 日期范围验证
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="起始日期不能晚于结束日期"
        )

    # 构建基础查询条件
    conditions = [
        ChannelMessage.channel_id == channel_id,
        ChannelMessage.is_deleted == False,
    ]

    # 如果用户被封禁，只能搜索封禁前的消息
    if member.is_banned and member.banned_at:
        conditions.append(ChannelMessage.created_at <= member.banned_at)

    # 关键词筛选
    if keyword:
        conditions.append(ChannelMessage.content.contains(keyword))

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

    # URL正则匹配模式
    URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'

    # 构建查询
    if content_type == "image_video":
        # 图片和视频筛选：JOIN附件表
        query = (
            select(ChannelMessage)
            .join(MessageAttachment, MessageAttachment.message_id == ChannelMessage.id)
            .where(and_(*conditions))
            .where(
                or_(
                    MessageAttachment.file_type.like("image/%"),
                    MessageAttachment.file_type.like("video/%")
                )
            )
            .options(
                selectinload(ChannelMessage.user),
                selectinload(ChannelMessage.attachments)
            )
            .distinct()
            .order_by(ChannelMessage.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        # 总数查询
        count_query = (
            select(func.count(func.distinct(ChannelMessage.id)))
            .select_from(ChannelMessage)
            .join(MessageAttachment, MessageAttachment.message_id == ChannelMessage.id)
            .where(and_(*conditions))
            .where(
                or_(
                    MessageAttachment.file_type.like("image/%"),
                    MessageAttachment.file_type.like("video/%")
                )
            )
        )
    elif content_type == "file":
        # 文件筛选：排除图片/视频/音频
        query = (
            select(ChannelMessage)
            .join(MessageAttachment, MessageAttachment.message_id == ChannelMessage.id)
            .where(and_(*conditions))
            .where(
                ~MessageAttachment.file_type.like("image/%"),
                ~MessageAttachment.file_type.like("video/%"),
                ~MessageAttachment.file_type.like("audio/%")
            )
            .options(
                selectinload(ChannelMessage.user),
                selectinload(ChannelMessage.attachments)
            )
            .distinct()
            .order_by(ChannelMessage.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        # 总数查询
        count_query = (
            select(func.count(func.distinct(ChannelMessage.id)))
            .select_from(ChannelMessage)
            .join(MessageAttachment, MessageAttachment.message_id == ChannelMessage.id)
            .where(and_(*conditions))
            .where(
                ~MessageAttachment.file_type.like("image/%"),
                ~MessageAttachment.file_type.like("video/%"),
                ~MessageAttachment.file_type.like("audio/%")
            )
        )
    elif content_type == "link":
        # 链接筛选：正则匹配URL
        conditions.append(ChannelMessage.content.op('~')(URL_PATTERN))
        query = (
            select(ChannelMessage)
            .where(and_(*conditions))
            .options(
                selectinload(ChannelMessage.user),
                selectinload(ChannelMessage.attachments)
            )
            .order_by(ChannelMessage.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        count_query = select(func.count(ChannelMessage.id)).where(and_(*conditions))
    else:
        # 普通关键词搜索
        query = (
            select(ChannelMessage)
            .where(and_(*conditions))
            .options(
                selectinload(ChannelMessage.user),
                selectinload(ChannelMessage.attachments)
            )
            .order_by(ChannelMessage.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        count_query = select(func.count(ChannelMessage.id)).where(and_(*conditions))

    # 执行搜索
    search_result = await db.execute(query)
    messages = search_result.scalars().all()

    # 获取总数
    total_result = await db.execute(count_query)
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
            "user_title_color": member.title_color if member else None,
            # 添加附件信息
            "attachments": [
                {
                    "id": str(att.id),
                    "fileName": att.file_name,
                    "fileType": att.file_type,
                    "fileSize": att.file_size,
                    "fileUrl": att.file_url,
                    "thumbnailUrl": att.thumbnail_url
                }
                for att in msg.attachments
            ] if msg.attachments else []
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
    禁言成员（owner 和 admin 可操作）
    - owner 可以禁言 admin 和 member
    - admin 只能禁言 member
    """
    # 检查操作者权限
    operator_member = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    operator = operator_member.scalar_one_or_none()

    if not operator or operator.role not in ['owner', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以禁言成员"
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

    # admin 不能禁言其他 admin
    if operator.role == 'admin' and target_member.role == 'admin':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="管理员不能禁言其他管理员"
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
    取消禁言（owner 和 admin 可操作）
    """
    # 检查操作者权限
    operator_member = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    operator = operator_member.scalar_one_or_none()

    if not operator or operator.role not in ['owner', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以取消禁言"
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


# ===== 消息反应（Emoji Reactions）相关 API =====

from app.models.message_reaction import MessageReaction
from app.schemas.channel import (
    ReactionCreate,
    ReactionSummary,
    ReactionDetailResponse,
    ReactionUserResponse,
    MessageReactionsResponse,
)


@router.post("/{channel_id}/messages/{message_id}/reactions")
async def add_reaction(
    channel_id: UUID,
    message_id: UUID,
    data: ReactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    添加消息反应（Emoji）
    """
    # 检查是否是频道成员
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 检查是否被封禁
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法操作"
        )

    # 检查消息是否存在且未删除
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
    if message.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="消息已被删除"
        )

    # 检查用户对该消息的不同 emoji 反应数量（限制20个）
    existing_count_result = await db.execute(
        select(func.count(MessageReaction.id)).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == current_user.id
        )
    )
    existing_count = existing_count_result.scalar() or 0
    if existing_count >= 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="每条消息最多可添加20个不同的反应"
        )

    # 检查是否已存在相同反应
    existing_reaction = await db.execute(
        select(MessageReaction).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == current_user.id,
            MessageReaction.emoji == data.emoji
        )
    )
    if existing_reaction.scalar_one_or_none():
        return {"message": "已添加该反应", "action": "exists"}

    # 创建反应
    reaction = MessageReaction(
        id=uuid.uuid4(),
        message_id=message_id,
        user_id=current_user.id,
        emoji=data.emoji
    )
    db.add(reaction)

    # 更新消息的 reaction_count
    message.reaction_count += 1

    await db.commit()

    # WebSocket 广播反应添加
    from app.api.v1.ws import broadcast_channel_event
    await broadcast_channel_event(channel_id, {
        "type": "REACTION_ADD",
        "payload": {
            "message_id": str(message_id),
            "emoji": data.emoji,
            "user_id": str(current_user.id),
            "username": current_user.username
        }
    })

    return {"message": "反应已添加", "action": "added"}


@router.delete("/{channel_id}/messages/{message_id}/reactions/{emoji}")
async def remove_reaction(
    channel_id: UUID,
    message_id: UUID,
    emoji: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    移除消息反应（只能移除自己的）
    """
    # 检查是否是频道成员
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 检查是否被封禁
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法操作"
        )

    # 查找反应
    reaction_result = await db.execute(
        select(MessageReaction).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == current_user.id,
            MessageReaction.emoji == emoji
        )
    )
    reaction = reaction_result.scalar_one_or_none()

    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反应不存在"
        )

    # 删除反应
    await db.delete(reaction)

    # 更新消息的 reaction_count
    message_result = await db.execute(
        select(ChannelMessage).where(ChannelMessage.id == message_id)
    )
    message = message_result.scalar_one_or_none()
    if message and message.reaction_count > 0:
        message.reaction_count -= 1

    await db.commit()

    # WebSocket 广播反应移除
    from app.api.v1.ws import broadcast_channel_event
    await broadcast_channel_event(channel_id, {
        "type": "REACTION_REMOVE",
        "payload": {
            "message_id": str(message_id),
            "emoji": emoji,
            "user_id": str(current_user.id)
        }
    })

    return {"message": "反应已移除"}


@router.get("/{channel_id}/messages/{message_id}/reactions", response_model=MessageReactionsResponse)
async def get_message_reactions(
    channel_id: UUID,
    message_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取消息的所有反应汇总
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

    # 检查消息是否存在
    message_result = await db.execute(
        select(ChannelMessage).where(
            ChannelMessage.id == message_id,
            ChannelMessage.channel_id == channel_id
        )
    )
    if not message_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )

    # 按 emoji 分组统计
    reactions_result = await db.execute(
        select(
            MessageReaction.emoji,
            func.count(MessageReaction.id).label('count')
        )
        .where(MessageReaction.message_id == message_id)
        .group_by(MessageReaction.emoji)
        .order_by(func.count(MessageReaction.id).desc())
    )
    reaction_stats = reactions_result.all()

    # 获取当前用户的反应
    user_reactions_result = await db.execute(
        select(MessageReaction.emoji).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == current_user.id
        )
    )
    user_emojis = set(row[0] for row in user_reactions_result.all())

    # 构建响应
    reactions = []
    total_count = 0
    for emoji, count in reaction_stats:
        reactions.append(ReactionSummary(
            emoji=emoji,
            count=count,
            has_reacted=(emoji in user_emojis)
        ))
        total_count += count

    return MessageReactionsResponse(
        message_id=message_id,
        reactions=reactions,
        total_count=total_count
    )


@router.get("/{channel_id}/messages/{message_id}/reactions/{emoji}/users")
async def get_reaction_users(
    channel_id: UUID,
    message_id: UUID,
    emoji: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取指定 emoji 反应的用户列表（点击 emoji 时调用）
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

    # 查询该 emoji 的所有反应
    reactions_result = await db.execute(
        select(MessageReaction)
        .where(
            MessageReaction.message_id == message_id,
            MessageReaction.emoji == emoji
        )
        .options(selectinload(MessageReaction.user))
        .order_by(MessageReaction.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    reactions = reactions_result.scalars().all()

    # 获取总数
    total_result = await db.execute(
        select(func.count(MessageReaction.id)).where(
            MessageReaction.message_id == message_id,
            MessageReaction.emoji == emoji
        )
    )
    total = total_result.scalar() or 0

    # 构建用户列表
    users = []
    for reaction in reactions:
        if reaction.user:
            users.append(ReactionUserResponse(
                user_id=reaction.user.id,
                username=reaction.user.username,
                avatar=reaction.user.avatar
            ))

    return ReactionDetailResponse(
        emoji=emoji,
        count=total,
        users=users
    )


# ===== 消息置顶相关 API =====

from app.schemas.channel import PinnedMessageResponse, PinnedMessagesListResponse


@router.post("/{channel_id}/messages/{message_id}/pin")
async def pin_message(
    channel_id: UUID,
    message_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    置顶消息（仅 owner/admin 可操作）
    最多置顶 50 条消息
    """
    # 检查操作者权限
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    if member.role not in ['owner', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有频道管理员可以置顶消息"
        )

    # 检查是否被封禁
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法操作"
        )

    # 检查消息是否存在且未删除
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

    if message.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法置顶已删除的消息"
        )

    if message.is_pinned:
        return {"message": "消息已经是置顶状态", "action": "already_pinned"}

    # 检查置顶数量限制
    pinned_count_result = await db.execute(
        select(func.count(ChannelMessage.id)).where(
            ChannelMessage.channel_id == channel_id,
            ChannelMessage.is_pinned == True,
            ChannelMessage.is_deleted == False
        )
    )
    pinned_count = pinned_count_result.scalar() or 0

    if pinned_count >= 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="频道置顶消息已达上限（50条）"
        )

    # 置顶消息
    from datetime import datetime, timezone
    message.is_pinned = True
    message.pinned_at = datetime.now(timezone.utc)
    message.pinned_by = current_user.id

    await db.commit()

    # WebSocket 广播置顶事件
    from app.api.v1.ws import broadcast_channel_event
    await broadcast_channel_event(channel_id, {
        "type": "MESSAGE_PIN",
        "payload": {
            "message_id": str(message_id),
            "pinned_by": str(current_user.id),
            "pinned_by_name": current_user.username,
            "pinned_at": message.pinned_at.isoformat() if message.pinned_at else None
        }
    })

    return {"message": "消息已置顶", "action": "pinned"}


@router.delete("/{channel_id}/messages/{message_id}/pin")
async def unpin_message(
    channel_id: UUID,
    message_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消置顶消息（仅 owner/admin 可操作）
    """
    # 检查操作者权限
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    if member.role not in ['owner', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有频道管理员可以取消置顶"
        )

    # 检查是否被封禁
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法操作"
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

    if not message.is_pinned:
        return {"message": "消息未被置顶", "action": "not_pinned"}

    # 取消置顶
    message.is_pinned = False
    message.pinned_at = None
    message.pinned_by = None

    await db.commit()

    # WebSocket 广播取消置顶事件
    from app.api.v1.ws import broadcast_channel_event
    await broadcast_channel_event(channel_id, {
        "type": "MESSAGE_UNPIN",
        "payload": {
            "message_id": str(message_id),
            "unpinned_by": str(current_user.id)
        }
    })

    return {"message": "已取消置顶", "action": "unpinned"}


@router.get("/{channel_id}/pinned-messages", response_model=PinnedMessagesListResponse)
async def get_pinned_messages(
    channel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取频道的所有置顶消息
    按置顶时间倒序排列（最新置顶的在前）
    """
    # 检查是否是频道成员
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 构建查询条件
    conditions = [
        ChannelMessage.channel_id == channel_id,
        ChannelMessage.is_pinned == True,
        ChannelMessage.is_deleted == False
    ]

    # 如果用户被封禁，只能看到封禁前的置顶消息
    if member.is_banned and member.banned_at:
        conditions.append(ChannelMessage.created_at <= member.banned_at)

    # 获取所有置顶消息
    pinned_result = await db.execute(
        select(ChannelMessage)
        .where(*conditions)
        .options(
            selectinload(ChannelMessage.user),
            selectinload(ChannelMessage.pinned_by_user)
        )
        .order_by(ChannelMessage.pinned_at.desc())
        .limit(50)
    )
    messages = pinned_result.scalars().all()

    # 构建响应
    pinned_messages = []
    for msg in messages:
        pinned_messages.append(PinnedMessageResponse(
            id=msg.id,
            channel_id=msg.channel_id,
            content=msg.content,
            user_id=msg.user_id,
            user_name=msg.user.username if msg.user else "已删除用户",
            user_avatar=msg.user.avatar if msg.user else None,
            is_pinned=msg.is_pinned,
            pinned_at=msg.pinned_at,
            pinned_by=msg.pinned_by,
            pinned_by_name=msg.pinned_by_user.username if msg.pinned_by_user else None,
            created_at=msg.created_at
        ))

    return PinnedMessagesListResponse(
        messages=pinned_messages,
        total=len(pinned_messages)
    )


# ===== 文件/图片上传相关 API =====

from fastapi import UploadFile, File
from app.models.message_attachment import MessageAttachment
from app.schemas.channel import AttachmentResponse, AttachmentUploadResponse
from app.services.cos_service import get_cos_service

# 允许的文件类型
ALLOWED_FILE_TYPES = [
    # 图片
    'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp',
    # 文档
    'application/pdf', 'text/plain',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    # 压缩包
    'application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed',
    # 视频
    'video/mp4', 'video/webm',
    # 音频
    'audio/mpeg', 'audio/wav', 'audio/ogg',
]

# 最大文件大小 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/{channel_id}/upload", response_model=AttachmentUploadResponse)
async def upload_attachment(
    channel_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    上传文件/图片附件
    - 支持图片、文档、压缩包等格式
    - 最大文件大小 10MB
    - 返回附件信息，可用于发送消息时关联
    """
    # 检查是否是频道成员
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 检查是否被封禁
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法上传文件"
        )

    # 检查是否被禁言
    from datetime import datetime, timezone
    if member.is_muted:
        if member.muted_until and datetime.now(timezone.utc) >= member.muted_until:
            member.is_muted = False
            member.muted_until = None
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您已被禁言，无法上传文件"
            )

    # 检查文件类型
    content_type = file.content_type or 'application/octet-stream'
    if content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型: {content_type}"
        )

    # 读取文件内容
    content = await file.read()

    # 检查文件大小
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制（最大 10MB）"
        )

    # 上传到 COS
    try:
        cos_service = get_cos_service()
        file_url = await cos_service.upload_channel_attachment(
            channel_id=str(channel_id),
            filename=file.filename,
            content=content,
            content_type=content_type
        )
    except Exception as e:
        logger.error(f"上传文件失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="文件上传失败，请稍后重试"
        )

    # 创建附件记录（暂不关联消息，发送消息时再关联）
    attachment = MessageAttachment(
        id=uuid.uuid4(),
        channel_id=channel_id,
        user_id=current_user.id,
        message_id=None,  # 发送消息时再关联
        file_name=file.filename or "unnamed",
        file_type=content_type,
        file_size=len(content),
        file_url=file_url,
        thumbnail_url=file_url if content_type.startswith('image/') else None
    )
    db.add(attachment)
    await db.commit()
    await db.refresh(attachment)

    return AttachmentUploadResponse(
        id=attachment.id,
        file_name=attachment.file_name,
        file_type=attachment.file_type,
        file_size=attachment.file_size,
        file_url=attachment.file_url,
        thumbnail_url=attachment.thumbnail_url
    )


@router.post("/{channel_id}/messages-with-attachments")
async def send_message_with_attachments(
    channel_id: UUID,
    content: str = Query("", description="消息内容，可为空（纯附件消息）"),
    message_type: MessageType = Query("normal"),
    reply_to_id: Optional[UUID] = Query(None, description="回复的消息ID"),
    attachment_ids: List[UUID] = Query(default=[], description="附件ID列表"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发送带附件的消息
    - content 可为空（纯附件消息）
    - attachment_ids 为预先上传的附件ID列表
    """
    # 检查内容和附件至少有一个
    if not content.strip() and not attachment_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="消息内容和附件不能同时为空"
        )

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

    # 检查频道是否已锁定
    if channel.status == "locked":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="频道已锁定，无法发送消息"
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

    if not member:
        if channel.type == "official":
            # 先检查是否存在被封禁的记录（防止"复活"）
            banned_check = await db.execute(
                select(ChannelMember).where(
                    ChannelMember.channel_id == channel_id,
                    ChannelMember.user_id == current_user.id,
                    ChannelMember.is_banned == True
                )
            )
            if banned_check.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="您已被移出该频道，无法发送消息"
                )

            member_role = "owner" if current_user.is_admin else "member"
            member = ChannelMember(
                id=uuid.uuid4(),
                channel_id=channel_id,
                user_id=current_user.id,
                role=member_role,
                joined_at=func.now()
            )
            db.add(member)
            await db.flush()
            channel.member_count += 1
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="未加入该频道"
            )

    # 检查是否被封禁（官方频道踢出后的用户）
    if member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法发送消息"
        )

    # 检查是否被禁言
    from datetime import datetime, timezone
    if member.is_muted:
        if member.muted_until and datetime.now(timezone.utc) >= member.muted_until:
            member.is_muted = False
            member.muted_until = None
            await db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您已被禁言"
            )

    # 检查频道状态
    if channel.status == "locked":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="频道已折叠，无法发送消息"
        )

    # 检查慢速模式
    if channel.slowmode_interval and channel.slowmode_interval > 0:
        # 管理员和群主不受慢速模式限制
        if member.role not in ['owner', 'admin']:
            # 获取用户最后一条消息的时间
            last_msg_result = await db.execute(
                select(ChannelMessage.created_at)
                .where(
                    ChannelMessage.channel_id == channel_id,
                    ChannelMessage.user_id == current_user.id,
                    ChannelMessage.is_deleted == False
                )
                .order_by(ChannelMessage.created_at.desc())
                .limit(1)
            )
            last_msg_time = last_msg_result.scalar_one_or_none()

            if last_msg_time:
                from datetime import timedelta
                time_since_last = datetime.now(timezone.utc) - last_msg_time
                if time_since_last.total_seconds() < channel.slowmode_interval:
                    remaining = channel.slowmode_interval - int(time_since_last.total_seconds())
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"慢速模式已启用，请等待 {remaining} 秒后再发送消息"
                    )

    # 验证附件
    attachments = []
    if attachment_ids:
        attachments_result = await db.execute(
            select(MessageAttachment).where(
                MessageAttachment.id.in_(attachment_ids),
                MessageAttachment.channel_id == channel_id,
                MessageAttachment.user_id == current_user.id,
                MessageAttachment.message_id == None  # 只能关联未被使用的附件
            )
        )
        attachments = attachments_result.scalars().all()

        if len(attachments) != len(attachment_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="部分附件不存在或已被使用"
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

    # 创建消息（允许纯附件消息，内容为空）
    message_content = content.strip()
    message = ChannelMessage(
        id=uuid.uuid4(),
        channel_id=channel_id,
        user_id=current_user.id,
        content=message_content,
        type=message_type,
        reply_to_id=reply_to_id
    )
    db.add(message)
    await db.flush()

    # 关联附件到消息
    for attachment in attachments:
        attachment.message_id = message.id

    # 更新频道消息数和最后消息时间
    channel.message_count += 1
    channel.last_message_at = func.now()

    # 提取 @ 的用户名并更新未读计数
    mentioned_usernames = await extract_mentions(message_content, db)
    await update_unread_counts(db, channel_id, message.id, current_user.id, mentioned_usernames)

    await db.commit()
    await db.refresh(message)

    # WebSocket 广播新消息（包含附件信息，统一使用 camelCase）
    from app.api.v1.ws import broadcast_channel_message
    attachments_data = [
        {
            "id": str(att.id),
            "fileName": att.file_name,
            "fileType": att.file_type,
            "fileSize": att.file_size,
            "fileUrl": att.file_url,
            "thumbnailUrl": att.thumbnail_url
        }
        for att in attachments
    ]

    await broadcast_channel_message(channel_id, {
        "id": str(message.id),
        "channel_id": str(message.channel_id),
        "user_id": str(message.user_id),
        "content": message.content,
        "type": message.type,
        "is_pinned": message.is_pinned,
        "reply_to_id": str(message.reply_to_id) if message.reply_to_id else None,
        "forwarded_from_id": None,
        "reaction_count": message.reaction_count,
        "created_at": message.created_at.isoformat(),
        "user_name": current_user.username,
        "user_avatar": current_user.avatar,
        "user_bio": current_user.bio,
        "user_honor": current_user.honor,
        "user_title": member.custom_title,
        "user_title_color": member.title_color,
        "attachments": attachments_data
    }, exclude_user=current_user.id)

    # 返回时 attachments 也使用 camelCase（ApiAdapter 会转换外层但不转换数组内对象）
    attachments_response = [
        {
            "id": str(att.id),
            "fileName": att.file_name,
            "fileType": att.file_type,
            "fileSize": att.file_size,
            "fileUrl": att.file_url,
            "thumbnailUrl": att.thumbnail_url
        }
        for att in attachments
    ]

    return {
        "id": str(message.id),
        "channelId": str(message.channel_id),
        "userId": str(message.user_id),
        "userName": current_user.username,
        "userAvatar": current_user.avatar,
        "userBio": current_user.bio,
        "userTitle": member.custom_title,
        "userTitleColor": member.title_color,
        "content": message.content,
        "type": message.type,
        "isPinned": message.is_pinned,
        "replyToId": str(message.reply_to_id) if message.reply_to_id else None,
        "reactionCount": message.reaction_count,
        "createdAt": message.created_at.isoformat(),
        "attachments": attachments_response
    }


@router.get("/{channel_id}/messages/{message_id}/attachments")
async def get_message_attachments(
    channel_id: UUID,
    message_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取消息的附件列表"""
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

    # 获取附件
    attachments_result = await db.execute(
        select(MessageAttachment).where(
            MessageAttachment.message_id == message_id
        ).order_by(MessageAttachment.created_at)
    )
    attachments = attachments_result.scalars().all()

    return {
        "attachments": [
            {
                "id": str(att.id),
                "file_name": att.file_name,
                "file_type": att.file_type,
                "file_size": att.file_size,
                "file_url": att.file_url,
                "thumbnail_url": att.thumbnail_url,
                "created_at": att.created_at.isoformat()
            }
            for att in attachments
        ]
    }


# ===== 消息转发相关 API =====

from app.schemas.channel import ForwardMessageRequest, ForwardMessageResponse


@router.post("/{channel_id}/messages/{message_id}/forward", response_model=ForwardMessageResponse)
async def forward_message(
    channel_id: UUID,
    message_id: UUID,
    request: ForwardMessageRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    转发消息到其他频道
    - 最多可同时转发到 10 个频道
    - 需要是源频道成员
    - 需要是目标频道成员
    """
    logger.info(f"[转发消息] 用户 {current_user.id} 请求转发消息 {message_id} 从频道 {channel_id} 到 {len(request.target_channel_ids)} 个目标频道")

    # 检查源频道成员身份
    source_member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    source_member = source_member_result.scalar_one_or_none()
    if not source_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该频道成员"
        )

    # 检查是否被封禁
    if source_member.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被移出该频道，无法转发消息"
        )

    # 获取原始消息
    original_msg_result = await db.execute(
        select(ChannelMessage)
        .options(selectinload(ChannelMessage.user))
        .options(selectinload(ChannelMessage.channel))
        .options(selectinload(ChannelMessage.attachments))
        .where(
            ChannelMessage.id == message_id,
            ChannelMessage.channel_id == channel_id,
            ChannelMessage.is_deleted == False
        )
    )
    original_msg = original_msg_result.scalar_one_or_none()

    if not original_msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在或已删除"
        )

    # 检查目标频道成员身份
    target_members_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id.in_(request.target_channel_ids),
            ChannelMember.user_id == current_user.id
        )
    )
    target_members = target_members_result.scalars().all()
    valid_channel_ids = {m.channel_id for m in target_members}

    # 获取目标频道信息
    target_channels_result = await db.execute(
        select(Channel).where(
            Channel.id.in_(valid_channel_ids),
            Channel.status != 'locked'
        )
    )
    target_channels = target_channels_result.scalars().all()
    valid_channel_ids = {c.id for c in target_channels}

    failed_channels = [cid for cid in request.target_channel_ids if cid not in valid_channel_ids]
    forwarded_messages = []

    # 转发消息的 content 只存储用户评论，原消息信息通过 forwarded_from_id 关联
    forward_content = request.add_comment or ""

    # 准备原消息的附件信息
    original_attachments = []
    for att in original_msg.attachments:
        original_attachments.append({
            "id": str(att.id),
            "file_name": att.file_name,
            "file_type": att.file_type,
            "file_url": att.file_url,
            "thumbnail_url": att.thumbnail_url
        })

    # 构建 forwardedFrom 结构化数据
    forwarded_from_data = {
        "message_id": str(original_msg.id),
        "channel_id": str(original_msg.channel_id),
        "channel_name": original_msg.channel.name,
        "user_id": str(original_msg.user_id) if original_msg.user_id else None,
        "user_name": original_msg.user.username if original_msg.user else "已删除用户",
        "user_avatar": original_msg.user.avatar if original_msg.user else None,
        "user_bio": original_msg.user.bio if original_msg.user else None,
        "user_honor": original_msg.user.honor if original_msg.user else None,
        "content": original_msg.content,
        "created_at": original_msg.created_at.isoformat() if original_msg.created_at else None,
        "attachments": original_attachments
    }

    # 逐个频道转发
    for target_channel in target_channels:
        try:
            # 创建转发消息
            new_message = ChannelMessage(
                id=uuid.uuid4(),
                channel_id=target_channel.id,
                user_id=current_user.id,
                content=forward_content,
                type="normal",
                forwarded_from_id=original_msg.id
            )
            db.add(new_message)
            await db.flush()

            # 更新频道统计
            target_channel.message_count += 1
            target_channel.last_message_at = func.now()

            forwarded_messages.append({
                "channel_id": str(target_channel.id),
                "channel_name": target_channel.name,
                "message_id": str(new_message.id)
            })

            # WebSocket 广播
            from app.api.v1.ws import broadcast_channel_message
            await broadcast_channel_message(target_channel.id, {
                "id": str(new_message.id),
                "channel_id": str(new_message.channel_id),
                "user_id": str(current_user.id),
                "content": new_message.content,
                "type": new_message.type,
                "is_pinned": False,
                "reply_to_id": None,
                "forwarded_from_id": str(original_msg.id),
                "forwarded_from": forwarded_from_data,  # 结构化的转发来源信息
                "reaction_count": 0,
                "created_at": new_message.created_at.isoformat() if new_message.created_at else None,
                "user_name": current_user.username,
                "user_avatar": current_user.avatar,
                "user_bio": current_user.bio if hasattr(current_user, 'bio') else None,
                "user_honor": current_user.honor if hasattr(current_user, 'honor') else None,
                "user_title": None,
                "user_title_color": None,
                "attachments": []
            }, exclude_user=current_user.id)

        except Exception as e:
            logger.error(f"转发到频道 {target_channel.id} 失败: {e}")
            failed_channels.append(target_channel.id)

    await db.commit()

    logger.info(f"[转发消息] 转发完成: 成功 {len(forwarded_messages)} 个, 失败 {len(failed_channels)} 个")

    return ForwardMessageResponse(
        forwarded_count=len(forwarded_messages),
        failed_channels=failed_channels,
        messages=forwarded_messages
    )


@router.get("/{channel_id}/messages/{message_id}/forward-info")
async def get_forward_info(
    channel_id: UUID,
    message_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取转发消息的原始信息"""
    # 检查频道成员身份
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该频道成员"
        )

    # 获取消息
    msg_result = await db.execute(
        select(ChannelMessage)
        .options(selectinload(ChannelMessage.forwarded_from))
        .where(
            ChannelMessage.id == message_id,
            ChannelMessage.channel_id == channel_id
        )
    )
    message = msg_result.scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )

    if not message.forwarded_from_id:
        return {"is_forwarded": False, "original": None}

    # 获取原始消息信息
    original = message.forwarded_from
    if not original:
        return {"is_forwarded": True, "original": None, "original_deleted": True}

    # 获取原始频道和用户信息
    original_channel_result = await db.execute(
        select(Channel).where(Channel.id == original.channel_id)
    )
    original_channel = original_channel_result.scalar_one_or_none()

    original_user_result = await db.execute(
        select(User).where(User.id == original.user_id)
    )
    original_user = original_user_result.scalar_one_or_none()

    return {
        "is_forwarded": True,
        "original": {
            "message_id": str(original.id),
            "channel_id": str(original.channel_id),
            "channel_name": original_channel.name if original_channel else "已删除频道",
            "user_name": original_user.username if original_user else "已删除用户",
            "content": original.content,
            "created_at": original.created_at.isoformat()
        }
    }


# ===== 频道邀请链接 API =====

from app.models.channel_invite import ChannelInvite
from datetime import timedelta


@router.post("/{channel_id}/invites")
async def create_invite(
    channel_id: UUID,
    max_uses: Optional[int] = Query(None, ge=1, le=1000),
    expires_hours: Optional[int] = Query(None, ge=1, le=168),  # 最长7天
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建频道邀请链接"""
    # 检查是否是管理员或群主
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member or member.role not in ['owner', 'admin']:
        raise HTTPException(status_code=403, detail="只有管理员可以创建邀请链接")

    from datetime import datetime, timezone
    expires_at = None
    if expires_hours:
        expires_at = datetime.now(timezone.utc) + timedelta(hours=expires_hours)

    invite = ChannelInvite(
        channel_id=channel_id,
        creator_id=current_user.id,
        max_uses=max_uses,
        expires_at=expires_at
    )
    db.add(invite)
    await db.commit()
    await db.refresh(invite)

    return {
        "id": str(invite.id),
        "code": invite.code,
        "max_uses": invite.max_uses,
        "use_count": invite.use_count,
        "expires_at": invite.expires_at.isoformat() if invite.expires_at else None,
        "invite_url": f"/invite/{invite.code}"
    }


@router.get("/{channel_id}/invites")
async def list_invites(
    channel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取频道邀请链接列表"""
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member or member.role not in ['owner', 'admin']:
        raise HTTPException(status_code=403, detail="只有管理员可以查看邀请链接")

    invites_result = await db.execute(
        select(ChannelInvite)
        .options(selectinload(ChannelInvite.creator))
        .where(ChannelInvite.channel_id == channel_id, ChannelInvite.is_active == True)
        .order_by(ChannelInvite.created_at.desc())
    )
    invites = invites_result.scalars().all()

    return {
        "invites": [
            {
                "id": str(inv.id),
                "code": inv.code,
                "creator_name": inv.creator.username if inv.creator else None,
                "max_uses": inv.max_uses,
                "use_count": inv.use_count,
                "expires_at": inv.expires_at.isoformat() if inv.expires_at else None,
                "is_valid": inv.is_valid,
                "created_at": inv.created_at.isoformat()
            }
            for inv in invites
        ]
    }


@router.post("/join-by-invite/{invite_code}")
async def join_by_invite(
    invite_code: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """通过邀请链接加入频道"""
    invite_result = await db.execute(
        select(ChannelInvite)
        .options(selectinload(ChannelInvite.channel))
        .where(ChannelInvite.code == invite_code, ChannelInvite.is_active == True)
    )
    invite = invite_result.scalar_one_or_none()

    if not invite:
        raise HTTPException(status_code=404, detail="邀请链接不存在或已失效")

    if not invite.is_valid:
        raise HTTPException(status_code=400, detail="邀请链接已过期或已达到使用上限")

    # 检查频道状态
    if invite.channel.status == "locked":
        raise HTTPException(status_code=400, detail="频道已折叠，无法加入")

    # 检查是否已是成员
    existing = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == invite.channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    existing_member = existing.scalar_one_or_none()
    if existing_member:
        # 如果用户被封禁，拒绝重新加入
        if existing_member.is_banned:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您已被该频道踢出，无法重新加入"
            )
        return {"message": "您已是该频道成员", "channel_id": str(invite.channel_id)}

    # 加入频道
    member = ChannelMember(
        channel_id=invite.channel_id,
        user_id=current_user.id,
        role="member"
    )
    db.add(member)
    invite.use_count += 1
    invite.channel.member_count += 1

    await db.commit()

    return {
        "message": "成功加入频道",
        "channel_id": str(invite.channel_id),
        "channel_name": invite.channel.name
    }


# ===== 已读回执 API =====

@router.get("/{channel_id}/messages/{message_id}/readers")
async def get_message_readers(
    channel_id: UUID,
    message_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取已读消息的用户列表"""
    # 检查成员身份
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="您不是该频道成员")

    # 获取消息时间
    msg_result = await db.execute(
        select(ChannelMessage).where(ChannelMessage.id == message_id)
    )
    message = msg_result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")

    # 获取已读用户（last_read_at >= message.created_at 的用户）
    from app.models.channel_read_state import ChannelReadState
    readers_result = await db.execute(
        select(ChannelReadState, User)
        .join(User, ChannelReadState.user_id == User.id)
        .where(
            ChannelReadState.channel_id == channel_id,
            ChannelReadState.last_read_at >= message.created_at
        )
        .offset(skip)
        .limit(limit)
    )
    readers = readers_result.all()

    count_result = await db.execute(
        select(func.count(ChannelReadState.id)).where(
            ChannelReadState.channel_id == channel_id,
            ChannelReadState.last_read_at >= message.created_at
        )
    )
    total = count_result.scalar() or 0

    return {
        "readers": [
            {
                "user_id": str(user.id),
                "username": user.username,
                "avatar": user.avatar,
                "read_at": state.last_read_at.isoformat()
            }
            for state, user in readers
        ],
        "total": total
    }


# ===== 消息书签 API =====

from app.models.message_bookmark import MessageBookmark


@router.post("/{channel_id}/messages/{message_id}/bookmark")
async def add_bookmark(
    channel_id: UUID,
    message_id: UUID,
    note: Optional[str] = Query(None, max_length=500),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """收藏消息"""
    # 检查成员身份
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="您不是该频道成员")

    # 检查是否被封禁
    if member.is_banned:
        raise HTTPException(status_code=403, detail="您已被移出该频道")

    # 检查消息是否存在
    msg_result = await db.execute(
        select(ChannelMessage).where(
            ChannelMessage.id == message_id,
            ChannelMessage.channel_id == channel_id
        )
    )
    if not msg_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="消息不存在")

    # 检查是否已收藏
    existing = await db.execute(
        select(MessageBookmark).where(
            MessageBookmark.user_id == current_user.id,
            MessageBookmark.message_id == message_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="已收藏该消息")

    bookmark = MessageBookmark(
        user_id=current_user.id,
        message_id=message_id,
        channel_id=channel_id,
        note=note
    )
    db.add(bookmark)
    await db.commit()

    return {"message": "收藏成功", "bookmark_id": str(bookmark.id)}


@router.delete("/{channel_id}/messages/{message_id}/bookmark")
async def remove_bookmark(
    channel_id: UUID,
    message_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """取消收藏"""
    # 检查成员身份和封禁状态
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if member and member.is_banned:
        raise HTTPException(status_code=403, detail="您已被移出该频道")

    result = await db.execute(
        select(MessageBookmark).where(
            MessageBookmark.user_id == current_user.id,
            MessageBookmark.message_id == message_id
        )
    )
    bookmark = result.scalar_one_or_none()
    if not bookmark:
        raise HTTPException(status_code=404, detail="未收藏该消息")

    await db.delete(bookmark)
    await db.commit()

    return {"message": "已取消收藏"}


@router.get("/my-bookmarks")
async def get_my_bookmarks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取我的书签列表"""
    bookmarks_result = await db.execute(
        select(MessageBookmark)
        .options(
            selectinload(MessageBookmark.message),
            selectinload(MessageBookmark.channel)
        )
        .where(MessageBookmark.user_id == current_user.id)
        .order_by(MessageBookmark.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    bookmarks = bookmarks_result.scalars().all()

    count_result = await db.execute(
        select(func.count(MessageBookmark.id)).where(MessageBookmark.user_id == current_user.id)
    )
    total = count_result.scalar() or 0

    return {
        "bookmarks": [
            {
                "id": str(bm.id),
                "message_id": str(bm.message_id),
                "channel_id": str(bm.channel_id),
                "channel_name": bm.channel.name if bm.channel else None,
                "content": bm.message.content if bm.message else "[已删除]",
                "note": bm.note,
                "created_at": bm.created_at.isoformat()
            }
            for bm in bookmarks
        ],
        "total": total
    }


# ===== 慢速模式 API =====

@router.put("/{channel_id}/slowmode")
async def set_slowmode(
    channel_id: UUID,
    interval: Optional[int] = Query(None, ge=0, le=3600, description="慢速模式间隔(秒)，0或null表示关闭"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """设置频道慢速模式"""
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member or member.role not in ['owner', 'admin']:
        raise HTTPException(status_code=403, detail="只有管理员可以设置慢速模式")

    channel_result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = channel_result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="频道不存在")

    channel.slowmode_interval = interval if interval and interval > 0 else None
    await db.commit()

    return {
        "message": "慢速模式设置成功",
        "slowmode_interval": channel.slowmode_interval
    }


# ===== 自定义通知 API =====

from app.models.channel_notification_setting import ChannelNotificationSetting


@router.get("/{channel_id}/notification-settings")
async def get_notification_settings(
    channel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取频道通知设置"""
    result = await db.execute(
        select(ChannelNotificationSetting).where(
            ChannelNotificationSetting.channel_id == channel_id,
            ChannelNotificationSetting.user_id == current_user.id
        )
    )
    setting = result.scalar_one_or_none()

    if not setting:
        return {
            "is_muted": False,
            "mute_until": None,
            "notify_mentions": True,
            "notify_announcements": True
        }

    return {
        "is_muted": setting.is_muted,
        "mute_until": setting.mute_until.isoformat() if setting.mute_until else None,
        "notify_mentions": setting.notify_mentions,
        "notify_announcements": setting.notify_announcements
    }


@router.put("/{channel_id}/notification-settings")
async def update_notification_settings(
    channel_id: UUID,
    is_muted: Optional[bool] = Query(None),
    mute_hours: Optional[int] = Query(None, ge=1, le=8760),  # 最长1年
    notify_mentions: Optional[bool] = Query(None),
    notify_announcements: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新频道通知设置"""
    result = await db.execute(
        select(ChannelNotificationSetting).where(
            ChannelNotificationSetting.channel_id == channel_id,
            ChannelNotificationSetting.user_id == current_user.id
        )
    )
    setting = result.scalar_one_or_none()

    if not setting:
        setting = ChannelNotificationSetting(
            channel_id=channel_id,
            user_id=current_user.id
        )
        db.add(setting)

    if is_muted is not None:
        setting.is_muted = is_muted
        if is_muted and mute_hours:
            from datetime import datetime, timezone
            setting.mute_until = datetime.now(timezone.utc) + timedelta(hours=mute_hours)
        elif not is_muted:
            setting.mute_until = None

    if notify_mentions is not None:
        setting.notify_mentions = notify_mentions
    if notify_announcements is not None:
        setting.notify_announcements = notify_announcements

    await db.commit()
    await db.refresh(setting)

    return {
        "message": "设置已更新",
        "is_muted": setting.is_muted,
        "mute_until": setting.mute_until.isoformat() if setting.mute_until else None,
        "notify_mentions": setting.notify_mentions,
        "notify_announcements": setting.notify_announcements
    }


# ===== GIF/贴纸搜索 API =====

import httpx


@router.get("/gif/search")
async def search_gif(
    query: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_active_user)
):
    """搜索 GIF（使用 Giphy API）"""
    # 这里使用 Giphy API，需要配置 API KEY
    from app.core.config import settings
    giphy_api_key = getattr(settings, 'GIPHY_API_KEY', None)

    if not giphy_api_key:
        # 返回模拟数据或提示未配置
        return {
            "gifs": [],
            "total": 0,
            "message": "GIF 服务未配置"
        }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.giphy.com/v1/gifs/search",
                params={
                    "api_key": giphy_api_key,
                    "q": query,
                    "limit": limit,
                    "offset": offset,
                    "rating": "g",
                    "lang": "zh"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            return {
                "gifs": [
                    {
                        "id": gif["id"],
                        "title": gif.get("title", ""),
                        "url": gif["images"]["fixed_height"]["url"],
                        "preview_url": gif["images"]["fixed_height_small"]["url"],
                        "width": int(gif["images"]["fixed_height"]["width"]),
                        "height": int(gif["images"]["fixed_height"]["height"])
                    }
                    for gif in data.get("data", [])
                ],
                "total": data.get("pagination", {}).get("total_count", 0)
            }
    except Exception as e:
        logger.error(f"GIF 搜索失败: {e}")
        return {"gifs": [], "total": 0, "error": "搜索失败"}


@router.get("/gif/trending")
async def trending_gif(
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_active_user)
):
    """获取热门 GIF"""
    from app.core.config import settings
    giphy_api_key = getattr(settings, 'GIPHY_API_KEY', None)

    if not giphy_api_key:
        return {"gifs": [], "total": 0, "message": "GIF 服务未配置"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.giphy.com/v1/gifs/trending",
                params={
                    "api_key": giphy_api_key,
                    "limit": limit,
                    "offset": offset,
                    "rating": "g"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            return {
                "gifs": [
                    {
                        "id": gif["id"],
                        "title": gif.get("title", ""),
                        "url": gif["images"]["fixed_height"]["url"],
                        "preview_url": gif["images"]["fixed_height_small"]["url"],
                        "width": int(gif["images"]["fixed_height"]["width"]),
                        "height": int(gif["images"]["fixed_height"]["height"])
                    }
                    for gif in data.get("data", [])
                ],
                "total": data.get("pagination", {}).get("total_count", 0)
            }
    except Exception as e:
        logger.error(f"获取热门 GIF 失败: {e}")
        return {"gifs": [], "total": 0, "error": "获取失败"}

