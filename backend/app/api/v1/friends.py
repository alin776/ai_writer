"""好友系统 API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.friendship import Friendship
from app.models.friend_request import FriendRequest
from app.models.channel import Channel, ChannelType
from app.models.channel_member import ChannelMember, MemberRole
from app.schemas.friend import (
    FriendRequestCreate,
    FriendRequestAction,
    FriendRequestResponse,
    FriendRequestListResponse,
    FriendshipResponse,
    FriendListResponse,
    FriendCheckResponse,
    PendingCountResponse,
    PendingRequestInfo,
    AcceptRequestResponse,
    RejectRequestResponse,
    UserBrief,
)

router = APIRouter()


# ========== 辅助函数 ==========

def user_to_brief(user: User) -> UserBrief:
    """转换用户为简要信息"""
    return UserBrief(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        avatar=user.avatar
    )


def generate_private_channel_name(user_id_1: UUID, user_id_2: UUID) -> str:
    """生成私聊频道名称（排序保证唯一性）"""
    ids = sorted([str(user_id_1), str(user_id_2)])
    return f"{ids[0]}_{ids[1]}"


# ========== 好友请求 API ==========

@router.post("/request", response_model=FriendRequestResponse)
async def send_friend_request(
    request: FriendRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发送好友请求"""
    # 1. 不能添加自己
    if request.to_user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能添加自己为好友")

    # 2. 检查目标用户是否存在
    target_user = await db.get(User, request.to_user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 3. 检查是否已是好友
    existing_friendship = await db.execute(
        select(Friendship).where(
            Friendship.user_id == current_user.id,
            Friendship.friend_id == request.to_user_id
        )
    )
    if existing_friendship.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="已经是好友")

    # 4. 检查是否已有请求（我发给对方）
    existing_request = await db.execute(
        select(FriendRequest).where(
            FriendRequest.from_user_id == current_user.id,
            FriendRequest.to_user_id == request.to_user_id
        )
    )
    existing_req = existing_request.scalar_one_or_none()
    if existing_req:
        if existing_req.status == 'pending':
            raise HTTPException(status_code=400, detail="已发送过请求，请等待对方处理")
        elif existing_req.status == 'rejected':
            # 重新申请：更新状态和时间
            existing_req.status = 'pending'
            existing_req.message = request.message
            existing_req.updated_at = datetime.now()
            await db.commit()
            await db.refresh(existing_req)
            return FriendRequestResponse(
                id=existing_req.id,
                from_user=user_to_brief(current_user),
                to_user=user_to_brief(target_user),
                message=existing_req.message,
                status=existing_req.status,
                created_at=existing_req.created_at
            )

    # 5. 检查对方是否已向我发送请求
    reverse_request = await db.execute(
        select(FriendRequest).where(
            FriendRequest.from_user_id == request.to_user_id,
            FriendRequest.to_user_id == current_user.id,
            FriendRequest.status == 'pending'
        )
    )
    if reverse_request.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="对方已向你发送好友请求，请前往处理")

    # 6. 创建新请求
    friend_request = FriendRequest(
        from_user_id=current_user.id,
        to_user_id=request.to_user_id,
        message=request.message,
        status='pending'
    )
    db.add(friend_request)
    await db.commit()
    await db.refresh(friend_request)

    return FriendRequestResponse(
        id=friend_request.id,
        from_user=user_to_brief(current_user),
        to_user=user_to_brief(target_user),
        message=friend_request.message,
        status=friend_request.status,
        created_at=friend_request.created_at
    )


@router.get("/requests/received", response_model=FriendRequestListResponse)
async def get_received_requests(
    status: Optional[str] = Query("pending", description="筛选状态：pending/accepted/rejected/all"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取收到的好友请求"""
    query = select(FriendRequest).where(FriendRequest.to_user_id == current_user.id)

    if status and status != 'all':
        query = query.where(FriendRequest.status == status)

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # 获取列表
    query = query.order_by(FriendRequest.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    requests = result.scalars().all()

    # 获取发送者信息
    items = []
    for req in requests:
        from_user = await db.get(User, req.from_user_id)
        to_user = await db.get(User, req.to_user_id)
        items.append(FriendRequestResponse(
            id=req.id,
            from_user=user_to_brief(from_user),
            to_user=user_to_brief(to_user),
            message=req.message,
            status=req.status,
            created_at=req.created_at
        ))

    return FriendRequestListResponse(total=total, items=items)


@router.get("/requests/sent", response_model=FriendRequestListResponse)
async def get_sent_requests(
    status: Optional[str] = Query("pending", description="筛选状态：pending/accepted/rejected/all"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取发出的好友请求"""
    query = select(FriendRequest).where(FriendRequest.from_user_id == current_user.id)

    if status and status != 'all':
        query = query.where(FriendRequest.status == status)

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # 获取列表
    query = query.order_by(FriendRequest.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    requests = result.scalars().all()

    # 获取接收者信息
    items = []
    for req in requests:
        from_user = await db.get(User, req.from_user_id)
        to_user = await db.get(User, req.to_user_id)
        items.append(FriendRequestResponse(
            id=req.id,
            from_user=user_to_brief(from_user),
            to_user=user_to_brief(to_user),
            message=req.message,
            status=req.status,
            created_at=req.created_at
        ))

    return FriendRequestListResponse(total=total, items=items)


@router.put("/request/{request_id}")
async def handle_friend_request(
    request_id: UUID,
    action: FriendRequestAction,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """处理好友请求（同意/拒绝）"""
    # 1. 获取请求并验证
    friend_request = await db.get(FriendRequest, request_id)
    if not friend_request:
        raise HTTPException(status_code=404, detail="请求不存在")

    if friend_request.to_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权处理此请求")

    if friend_request.status != 'pending':
        raise HTTPException(status_code=400, detail="请求已处理")

    if action.action == 'reject':
        # 拒绝请求
        friend_request.status = 'rejected'
        friend_request.updated_at = datetime.now()
        await db.commit()
        return RejectRequestResponse(message="已拒绝好友请求")

    # 同意请求
    from_user = await db.get(User, friend_request.from_user_id)

    # 2. 检查是否存在历史私聊频道
    channel_name = generate_private_channel_name(friend_request.from_user_id, friend_request.to_user_id)
    existing_channel = await db.execute(
        select(Channel).where(
            Channel.name == channel_name,
            Channel.type == ChannelType.PRIVATE
        )
    )
    private_channel = existing_channel.scalar_one_or_none()

    if private_channel:
        # 复用历史频道
        if private_channel.status != 'active':
            private_channel.status = 'active'
    else:
        # 3. 创建私聊频道
        private_channel = Channel(
            name=channel_name,
            type=ChannelType.PRIVATE,
            creator_id=friend_request.from_user_id,
            is_permanent=True,
            member_count=2
        )
        db.add(private_channel)
        await db.flush()

        # 添加两个成员
        member1 = ChannelMember(
            channel_id=private_channel.id,
            user_id=friend_request.from_user_id,
            role=MemberRole.OWNER
        )
        member2 = ChannelMember(
            channel_id=private_channel.id,
            user_id=friend_request.to_user_id,
            role=MemberRole.MEMBER
        )
        db.add(member1)
        db.add(member2)

    # 4. 创建双向好友关系
    friendship1 = Friendship(
        user_id=friend_request.from_user_id,
        friend_id=friend_request.to_user_id,
        private_channel_id=private_channel.id
    )
    friendship2 = Friendship(
        user_id=friend_request.to_user_id,
        friend_id=friend_request.from_user_id,
        private_channel_id=private_channel.id
    )
    db.add(friendship1)
    db.add(friendship2)

    # 5. 更新请求状态
    friend_request.status = 'accepted'
    friend_request.updated_at = datetime.now()

    await db.commit()

    return AcceptRequestResponse(
        message="已同意好友请求",
        friendship=FriendshipResponse(
            id=friendship2.id,
            friend=user_to_brief(from_user),
            private_channel_id=private_channel.id,
            created_at=friendship2.created_at
        ),
        private_channel_id=private_channel.id
    )


@router.get("/requests/count", response_model=PendingCountResponse)
async def get_pending_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取待处理请求数量"""
    count_query = select(func.count()).where(
        FriendRequest.to_user_id == current_user.id,
        FriendRequest.status == 'pending'
    )
    count = (await db.execute(count_query)).scalar()
    return PendingCountResponse(pending_count=count)


# ========== 好友管理 API ==========

@router.get("", response_model=FriendListResponse)
async def get_friends(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取好友列表"""
    query = select(Friendship).where(Friendship.user_id == current_user.id)

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # 获取列表
    query = query.order_by(Friendship.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    friendships = result.scalars().all()

    # 获取好友信息和私聊频道的最后消息时间
    items = []
    for fs in friendships:
        friend = await db.get(User, fs.friend_id)

        # 获取私聊频道的最后消息时间
        last_message_at = None
        if fs.private_channel_id:
            channel = await db.get(Channel, fs.private_channel_id)
            if channel:
                last_message_at = channel.last_message_at

        items.append(FriendshipResponse(
            id=fs.id,
            friend=user_to_brief(friend),
            private_channel_id=fs.private_channel_id,
            last_message_at=last_message_at,
            created_at=fs.created_at
        ))

    return FriendListResponse(total=total, items=items)


@router.delete("/{friend_id}")
async def delete_friend(
    friend_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除好友"""
    # 1. 检查好友关系是否存在
    result = await db.execute(
        select(Friendship).where(
            Friendship.user_id == current_user.id,
            Friendship.friend_id == friend_id
        )
    )
    friendship = result.scalar_one_or_none()
    if not friendship:
        raise HTTPException(status_code=404, detail="好友关系不存在")

    # 2. 删除双向好友关系
    await db.execute(
        select(Friendship).where(
            Friendship.user_id == friend_id,
            Friendship.friend_id == current_user.id
        )
    )
    reverse_friendship = (await db.execute(
        select(Friendship).where(
            Friendship.user_id == friend_id,
            Friendship.friend_id == current_user.id
        )
    )).scalar_one_or_none()

    await db.delete(friendship)
    if reverse_friendship:
        await db.delete(reverse_friendship)

    # 3. 私聊频道保留（不删除历史消息）
    await db.commit()

    return {"message": "已删除好友"}


@router.get("/check/{user_id}", response_model=FriendCheckResponse)
async def check_friendship(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """检查好友关系"""
    # 检查是否是好友
    result = await db.execute(
        select(Friendship).where(
            Friendship.user_id == current_user.id,
            Friendship.friend_id == user_id
        )
    )
    friendship = result.scalar_one_or_none()

    if friendship:
        return FriendCheckResponse(
            is_friend=True,
            friendship_id=friendship.id,
            private_channel_id=friendship.private_channel_id
        )

    # 检查是否有待处理的请求
    # 我发出的请求
    sent_request = await db.execute(
        select(FriendRequest).where(
            FriendRequest.from_user_id == current_user.id,
            FriendRequest.to_user_id == user_id,
            FriendRequest.status == 'pending'
        )
    )
    sent_req = sent_request.scalar_one_or_none()
    if sent_req:
        return FriendCheckResponse(
            is_friend=False,
            pending_request=PendingRequestInfo(
                id=sent_req.id,
                direction="sent",
                status=sent_req.status
            )
        )

    # 我收到的请求
    received_request = await db.execute(
        select(FriendRequest).where(
            FriendRequest.from_user_id == user_id,
            FriendRequest.to_user_id == current_user.id,
            FriendRequest.status == 'pending'
        )
    )
    received_req = received_request.scalar_one_or_none()
    if received_req:
        return FriendCheckResponse(
            is_friend=False,
            pending_request=PendingRequestInfo(
                id=received_req.id,
                direction="received",
                status=received_req.status
            )
        )

    return FriendCheckResponse(is_friend=False)
