"""
WebSocket实时推送

功能:
- 推送评审任务进度
- 推送AI生成状态
- 推送用户通知
- 频道实时消息推送
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from starlette.websockets import WebSocketState
from celery.result import AsyncResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import asyncio
import json
import logging
from uuid import UUID
from typing import Dict, Set, Optional
from jose import JWTError, jwt

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.services.notification_service import NotificationService
from app.schemas.notification import UserNotificationResponse
from app.models.channel_member import ChannelMember
from app.models.channel import Channel
from app.models.channel_notification_setting import ChannelNotificationSetting
from app.models.user import User
import uuid as uuid_module

logger = logging.getLogger(__name__)

router = APIRouter()

# 存储活跃的通知WebSocket连接 {user_id: Set[WebSocket]}
active_notification_connections: Dict[UUID, Set[WebSocket]] = {}

# 频道WebSocket连接存储 {channel_id: {user_id: WebSocket}}
active_channel_connections: Dict[UUID, Dict[UUID, WebSocket]] = {}

# 用户->频道反向映射 {user_id: Set[channel_id]}
user_channel_map: Dict[UUID, Set[UUID]] = {}

# 用户在线状态存储 {user_id: online_status}
user_online_status: Dict[UUID, str] = {}


# ============ JWT Token 验证 (WebSocket专用) ============

async def verify_ws_token(token: str) -> Optional[UUID]:
    """
    验证WebSocket连接的JWT Token

    Returns:
        user_id 或 None（验证失败）
    """
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            return None
        return UUID(user_id)
    except (JWTError, ValueError):
        return None


async def check_channel_member(channel_id: UUID, user_id: UUID) -> Optional[ChannelMember]:
    """
    检查用户是否为频道成员
    对于官方频道，如果用户没有成员记录会自动创建
    被封禁的用户返回 None

    Returns:
        ChannelMember 或 None
    """
    async with AsyncSessionLocal() as db:
        # 检查是否已是成员
        result = await db.execute(
            select(ChannelMember).where(
                ChannelMember.channel_id == channel_id,
                ChannelMember.user_id == user_id
            )
        )
        member = result.scalar_one_or_none()

        if member:
            # 检查是否被封禁
            if member.is_banned:
                return None  # 被封禁用户拒绝访问
            return member

        # 检查是否是官方频道
        channel_result = await db.execute(
            select(Channel).where(Channel.id == channel_id)
        )
        channel = channel_result.scalar_one_or_none()

        if channel and channel.type == "official":
            # 先检查是否存在被封禁的记录（防止"复活"）
            banned_check = await db.execute(
                select(ChannelMember).where(
                    ChannelMember.channel_id == channel_id,
                    ChannelMember.user_id == user_id,
                    ChannelMember.is_banned == True
                )
            )
            if banned_check.scalar_one_or_none():
                return None  # 被封禁用户拒绝访问

            # 获取用户信息判断角色
            user_result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = user_result.scalar_one_or_none()

            member_role = "owner" if user and user.is_admin else "member"

            try:
                # 自动创建成员记录
                member = ChannelMember(
                    id=uuid_module.uuid4(),
                    channel_id=channel_id,
                    user_id=user_id,
                    role=member_role
                )
                db.add(member)
                channel.member_count += 1
                await db.commit()
                await db.refresh(member)
                return member
            except IntegrityError:
                # 竞态条件：其他请求已创建成员记录，回滚后重新查询
                await db.rollback()
                result = await db.execute(
                    select(ChannelMember).where(
                        ChannelMember.channel_id == channel_id,
                        ChannelMember.user_id == user_id
                    )
                )
                member = result.scalar_one_or_none()
                # 再次检查是否被封禁
                if member and member.is_banned:
                    return None
                return member

        return None


@router.websocket("/ws/review/{task_id}")
async def review_progress(websocket: WebSocket, task_id: str):
    """
    实时推送评审进度

    消息格式:
    {
        "state": "PROGRESS",  # PENDING/PROGRESS/SUCCESS/FAILURE
        "progress": 45,       # 0-100
        "message": "正在分析第10章...",
        "current": 10,        # 当前进度
        "total": 20          # 总任务数
    }

    Args:
        websocket: WebSocket连接
        task_id: Celery任务ID
    """
    await websocket.accept()
    logger.info(f"[WebSocket] 客户端连接: task_id={task_id}")

    try:
        task = AsyncResult(task_id)

        while True:
            # 获取任务状态
            state = task.state

            if state == 'PENDING':
                await websocket.send_json({
                    "state": "PENDING",
                    "progress": 0,
                    "message": "任务排队中..."
                })

            elif state == 'PROGRESS':
                meta = task.info or {}
                await websocket.send_json({
                    "state": "PROGRESS",
                    "progress": meta.get('progress', 0),
                    "message": meta.get('message', '处理中...'),
                    "current": meta.get('current', 0),
                    "total": meta.get('total', 100)
                })

            elif state == 'SUCCESS':
                await websocket.send_json({
                    "state": "SUCCESS",
                    "progress": 100,
                    "message": "评审完成",
                    "result": task.result
                })
                logger.info(f"[WebSocket] 任务完成: task_id={task_id}")
                break

            elif state == 'FAILURE':
                error_msg = str(task.info) if task.info else "未知错误"
                await websocket.send_json({
                    "state": "FAILURE",
                    "progress": 0,
                    "message": f"任务失败: {error_msg}",
                    "error": error_msg
                })
                logger.error(f"[WebSocket] 任务失败: task_id={task_id}, error={error_msg}")
                break

            # 每秒更新一次
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        logger.info(f"[WebSocket] 客户端断开连接: task_id={task_id}")
    except Exception as e:
        logger.error(f"[WebSocket] 错误: {e}")
        try:
            await websocket.send_json({
                "state": "ERROR",
                "message": f"WebSocket错误: {str(e)}"
            })
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass


@router.websocket("/ws/test")
async def test_websocket(websocket: WebSocket):
    """
    测试WebSocket连接

    简单的echo服务,返回接收到的消息
    """
    await websocket.accept()
    logger.info("[WebSocket] 测试连接建立")

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"[WebSocket] 收到消息: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        logger.info("[WebSocket] 测试连接断开")


@router.websocket("/ws/notifications/{user_id}")
async def notifications_stream(websocket: WebSocket, user_id: str):
    """
    实时推送用户通知

    连接建立后:
    1. 立即发送未读通知列表
    2. 保持连接，实时推送新通知

    消息格式:
    {
        "type": "notification",  # notification/unread_count
        "data": {
            "id": "uuid",
            "title": "通知标题",
            "content": "通知内容",
            "priority": "important",
            "display_type": ["modal"],
            ...
        }
    }
    或
    {
        "type": "unread_count",
        "data": {
            "count": 5
        }
    }

    Args:
        websocket: WebSocket连接
        user_id: 用户ID
    """
    await websocket.accept()
    logger.info(f"[WebSocket] 通知连接建立: user_id={user_id}")

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        await websocket.send_json({
            "type": "error",
            "message": "Invalid user_id format"
        })
        await websocket.close()
        return

    # 注册连接
    if user_uuid not in active_notification_connections:
        active_notification_connections[user_uuid] = set()
    active_notification_connections[user_uuid].add(websocket)

    try:
        # 发送初始的未读数量
        # 注意：这里需要创建临时的数据库会话
        from app.core.database import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            notification_service = NotificationService(db)
            unread_count = await notification_service.get_unread_count(user_uuid)

            await websocket.send_json({
                "type": "unread_count",
                "data": {
                    "count": unread_count
                }
            })

            # 发送未读通知列表（最近10条）
            notifications, _, _ = await notification_service.get_user_notifications(
                user_id=user_uuid,
                skip=0,
                limit=10,
                is_read=False
            )

            if notifications:
                # 将 SQLAlchemy 模型转换为 Pydantic 模型，然后序列化为字典
                serialized_notifications = [
                    UserNotificationResponse.model_validate(notif).model_dump(mode='json')
                    for notif in notifications
                ]

                await websocket.send_json({
                    "type": "notifications_list",
                    "data": {
                        "notifications": serialized_notifications
                    }
                })

        # 保持连接，等待客户端消息或新通知推送
        while True:
            try:
                # 设置超时，避免完全阻塞
                message = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # 处理客户端发来的心跳或其他消息
                data = json.loads(message)
                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                # 发送心跳
                await websocket.send_json({"type": "heartbeat"})
            except WebSocketDisconnect:
                break

    except WebSocketDisconnect:
        logger.info(f"[WebSocket] 通知连接断开: user_id={user_id}")
    except asyncio.CancelledError:
        # 任务被取消（如服务器关闭），静默处理
        logger.debug(f"[WebSocket] 连接任务被取消: user_id={user_id}")
    except Exception as e:
        # 检查是否是连接已关闭的错误（常见于客户端断开）
        error_str = str(e).lower()
        exc_type_name = type(e).__name__.lower()
        is_connection_closed = any(keyword in error_str or keyword in exc_type_name for keyword in [
            "connectionclosed", "connection closed", "no close frame",
            "incomplete read", "clientdisconnected", "disconnected"
        ])

        if is_connection_closed:
            # 连接关闭是正常情况，降级为 DEBUG 日志
            logger.debug(f"[WebSocket] 连接已关闭: user_id={user_id}, reason={type(e).__name__}")
        else:
            # 其他错误才记录为 ERROR
            logger.error(f"[WebSocket] 通知推送错误: {type(e).__name__}: {e}")
            try:
                # 尝试发送错误消息前检查连接状态（使用枚举值比较更安全）
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"WebSocket error: {str(e)}"
                    })
            except Exception:
                pass  # 发送失败时静默处理
    finally:
        # 移除连接
        if user_uuid in active_notification_connections:
            active_notification_connections[user_uuid].discard(websocket)
            if not active_notification_connections[user_uuid]:
                del active_notification_connections[user_uuid]
        try:
            # 只在连接仍然打开时尝试关闭（使用枚举值比较更安全）
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.close()
        except Exception:
            pass  # 关闭失败时静默处理


async def broadcast_notification(user_id: UUID, notification_data: dict):
    """
    向指定用户的所有WebSocket连接广播通知

    Args:
        user_id: 用户ID
        notification_data: 通知数据
    """
    if user_id not in active_notification_connections:
        return

    # 向该用户的所有活跃连接发送通知
    disconnected_sockets = []
    for websocket in active_notification_connections[user_id]:
        try:
            # 2025-12-15: 发送前检查连接状态
            if websocket.client_state != WebSocketState.CONNECTED:
                disconnected_sockets.append(websocket)
                continue
            await websocket.send_json({
                "type": "notification",
                "data": notification_data
            })
        except Exception as e:
            logger.debug(f"[WebSocket] 发送通知失败: {e}")  # 降级为debug，避免日志污染
            disconnected_sockets.append(websocket)

    # 清理断开的连接
    for ws in disconnected_sockets:
        active_notification_connections[user_id].discard(ws)


async def broadcast_unread_count(user_id: UUID, count: int):
    """
    向指定用户的所有WebSocket连接广播未读数量更新

    Args:
        user_id: 用户ID
        count: 未读数量
    """
    if user_id not in active_notification_connections:
        return

    disconnected_sockets = []
    for websocket in active_notification_connections[user_id]:
        try:
            # 2025-12-15: 发送前检查连接状态
            if websocket.client_state != WebSocketState.CONNECTED:
                disconnected_sockets.append(websocket)
                continue
            await websocket.send_json({
                "type": "unread_count",
                "data": {
                    "count": count
                }
            })
        except Exception as e:
            logger.debug(f"[WebSocket] 发送未读数量失败: {e}")  # 降级为debug
            disconnected_sockets.append(websocket)

    # 清理断开的连接
    for ws in disconnected_sockets:
        active_notification_connections[user_id].discard(ws)


# ============ 频道 WebSocket ============

@router.websocket("/ws/channels/{channel_id}")
async def channel_stream(websocket: WebSocket, channel_id: str, token: str = Query(...)):
    """
    频道实时消息推送

    消息类型:
    - MESSAGE_NEW: 新消息
    - MESSAGE_DELETE: 消息撤回
    - TYPING: 正在输入
    - PRESENCE: 在线状态
    """
    # 1. 验证 JWT Token
    user_id = await verify_ws_token(token)
    if not user_id:
        await websocket.close(code=4001, reason="Invalid token")
        return

    # 2. 验证频道ID格式
    try:
        channel_uuid = UUID(channel_id)
    except ValueError:
        await websocket.close(code=4002, reason="Invalid channel_id")
        return

    # 3. 验证用户是否为频道成员（check_channel_member 已处理封禁用户，返回 None）
    member = await check_channel_member(channel_uuid, user_id)
    if not member:
        await websocket.close(code=4003, reason="Not a channel member or banned")
        return

    # 3.5 获取用户的在线状态
    async with AsyncSessionLocal() as db:
        user = await db.get(User, user_id)
        user_status = user.online_status if user else 'online'

    # 存储用户状态
    user_online_status[user_id] = user_status

    # 4. 接受连接
    await websocket.accept()

    # 5. 注册连接
    if channel_uuid not in active_channel_connections:
        active_channel_connections[channel_uuid] = {}
    active_channel_connections[channel_uuid][user_id] = websocket

    if user_id not in user_channel_map:
        user_channel_map[user_id] = set()
    user_channel_map[user_id].add(channel_uuid)

    # 6. 广播用户上线（隐身用户不广播）
    if user_status != 'offline':
        await broadcast_channel_event(channel_uuid, {
            "type": "PRESENCE",
            "payload": {"user_id": str(user_id), "status": user_status}
        }, exclude_user=user_id)

    # 7. 发送当前在线用户列表给新连接的用户
    online_users = get_channel_online_users(channel_uuid)
    await websocket.send_json({
        "type": "ONLINE_USERS",
        "payload": {"users": online_users}
    })

    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                data = json.loads(message)
                msg_type = data.get("type")

                if msg_type == "ping":
                    await websocket.send_json({"type": "pong"})
                elif msg_type == "TYPING" and not member.is_muted and not member.is_banned:
                    await broadcast_channel_event(channel_uuid, {
                        "type": "TYPING",
                        "payload": {"user_id": str(user_id), "username": data.get("username", "")}
                    }, exclude_user=user_id)

            except asyncio.TimeoutError:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json({"type": "heartbeat"})

    except WebSocketDisconnect:
        pass
    except asyncio.CancelledError:
        pass
    except Exception as e:
        if "closed" not in str(e).lower():
            logger.error(f"[Channel WS] 错误: {e}")
    finally:
        # 清理连接
        if channel_uuid in active_channel_connections:
            active_channel_connections[channel_uuid].pop(user_id, None)
            if not active_channel_connections[channel_uuid]:
                del active_channel_connections[channel_uuid]
        if user_id in user_channel_map:
            user_channel_map[user_id].discard(channel_uuid)
            if not user_channel_map[user_id]:
                del user_channel_map[user_id]

        # 广播用户离线（隐身用户不广播）
        stored_status = user_online_status.get(user_id, 'online')
        if stored_status != 'offline':
            await broadcast_channel_event(channel_uuid, {
                "type": "PRESENCE",
                "payload": {"user_id": str(user_id), "status": "offline"}
            })

        # 清理用户状态（如果用户没有其他频道连接）
        if user_id not in user_channel_map:
            user_online_status.pop(user_id, None)

        try:
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.close()
        except:
            pass


async def broadcast_channel_event(channel_id: UUID, event_data: dict, exclude_user: UUID = None):
    """向频道内所有用户广播事件"""
    if channel_id not in active_channel_connections:
        return

    disconnected = []
    for uid, ws in active_channel_connections[channel_id].items():
        if exclude_user and uid == exclude_user:
            continue
        try:
            if ws.client_state == WebSocketState.CONNECTED:
                await ws.send_json(event_data)
            else:
                disconnected.append(uid)
        except Exception as e:
            logger.error(f"[Channel WS] 发送消息给 {uid} 失败: {e}")
            disconnected.append(uid)

    for uid in disconnected:
        active_channel_connections[channel_id].pop(uid, None)


async def broadcast_channel_message(channel_id: UUID, message_data: dict, exclude_user: UUID = None):
    """广播新消息到频道（过滤静音用户）"""
    if channel_id not in active_channel_connections:
        return

    # 获取在线用户列表
    online_user_ids = list(active_channel_connections[channel_id].keys())
    if not online_user_ids:
        return

    # 查询哪些在线用户静音了该频道
    muted_user_ids = set()
    try:
        async with AsyncSessionLocal() as db:
            from sqlalchemy import select
            result = await db.execute(
                select(ChannelNotificationSetting.user_id).where(
                    ChannelNotificationSetting.channel_id == channel_id,
                    ChannelNotificationSetting.user_id.in_(online_user_ids),
                    ChannelNotificationSetting.is_muted == True
                )
            )
            muted_user_ids = {row[0] for row in result.fetchall()}
    except Exception as e:
        logger.error(f"[Channel WS] 查询静音用户失败: {e}")

    # 广播消息，排除静音用户
    event_data = {"type": "MESSAGE_NEW", "payload": message_data}
    disconnected = []

    for uid, ws in active_channel_connections[channel_id].items():
        if exclude_user and uid == exclude_user:
            continue
        if uid in muted_user_ids:
            continue
        try:
            if ws.client_state == WebSocketState.CONNECTED:
                await ws.send_json(event_data)
            else:
                disconnected.append(uid)
        except Exception as e:
            logger.error(f"[Channel WS] 发送消息给 {uid} 失败: {e}")
            disconnected.append(uid)

    for uid in disconnected:
        active_channel_connections[channel_id].pop(uid, None)


async def broadcast_message_delete(channel_id: UUID, message_id: str):
    """广播消息撤回事件"""
    await broadcast_channel_event(channel_id, {"type": "MESSAGE_DELETE", "payload": {"message_id": message_id}})


async def broadcast_message_edit(
    channel_id: UUID,
    message_id: str,
    content: str,
    user_id: str,
    user_name: str,
    edited_at: str = None
):
    """广播消息编辑事件"""
    await broadcast_channel_event(channel_id, {
        "type": "MESSAGE_EDIT",
        "payload": {
            "channel_id": str(channel_id),
            "message_id": message_id,
            "content": content,
            "user_id": user_id,
            "user_name": user_name,
            "edited_at": edited_at,
            "is_edited": True
        }
    })


def get_channel_online_users(channel_id: UUID) -> list:
    """获取频道在线用户列表（排除隐身用户）"""
    if channel_id not in active_channel_connections:
        return []
    # 排除隐身用户（状态为 'offline'）
    return [
        str(uid) for uid in active_channel_connections[channel_id].keys()
        if user_online_status.get(uid, 'online') != 'offline'
    ]


async def update_user_online_status(user_id: UUID, new_status: str):
    """
    更新用户在线状态并广播到所有相关频道

    Args:
        user_id: 用户ID
        new_status: 新的在线状态 ('online', 'idle', 'dnd', 'offline')
    """
    old_status = user_online_status.get(user_id, 'online')
    user_online_status[user_id] = new_status

    # 获取用户所在的所有频道
    user_channels = user_channel_map.get(user_id, set())

    # 广播到每个频道
    for channel_id in user_channels:
        # 如果用户变为隐身，广播 offline；否则广播真实状态
        broadcast_status = 'offline' if new_status == 'offline' else new_status

        # 如果用户从隐身变为可见，广播 online 状态
        if old_status == 'offline' and new_status != 'offline':
            broadcast_status = new_status

        await broadcast_channel_event(channel_id, {
            "type": "PRESENCE",
            "payload": {
                "user_id": str(user_id),
                "status": broadcast_status
            }
        }, exclude_user=user_id)

