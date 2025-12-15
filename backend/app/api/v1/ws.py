"""
WebSocket实时推送

功能:
- 推送评审任务进度
- 推送AI生成状态
- 推送用户通知
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from starlette.websockets import WebSocketState  # 2025-12-15: 导入用于安全的连接状态检查
from celery.result import AsyncResult
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import json
import logging
from uuid import UUID
from typing import Dict, Set

from app.core.database import get_db
from app.services.notification_service import NotificationService
from app.schemas.notification import UserNotificationResponse

logger = logging.getLogger(__name__)

router = APIRouter()

# 存储活跃的通知WebSocket连接 {user_id: Set[WebSocket]}
active_notification_connections: Dict[UUID, Set[WebSocket]] = {}


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
        is_connection_closed = any(keyword in error_str for keyword in [
            "connectionclosed", "connection closed", "no close frame",
            "incomplete read", "clientdisconnected", "disconnected"
        ])

        if is_connection_closed:
            # 连接关闭是正常情况，降级为 DEBUG 日志
            logger.debug(f"[WebSocket] 连接已关闭: user_id={user_id}, reason={type(e).__name__}")
        else:
            # 其他错误才记录为 ERROR
            logger.error(f"[WebSocket] 通知推送错误: {e}", exc_info=True)
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

