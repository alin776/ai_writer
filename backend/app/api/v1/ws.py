"""
WebSocket实时推送

功能:
- 推送评审任务进度
- 推送AI生成状态
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from celery.result import AsyncResult
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


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
