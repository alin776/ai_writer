"""
请求上下文管理

使用 Python contextvars 在异步调用链中传播请求级别的上下文信息（db会话和user_id），
无需在每个函数签名中显式传递参数。

主要用途：
- 为全局Agent实例提供用户上下文，实现成本追踪
- 支持编辑器工具等全局服务的用户级别操作

创建日期：2025-12-01
"""

from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# 请求级别的上下文变量（自动在异步调用链中传播）
request_db: ContextVar[Optional[AsyncSession]] = ContextVar('request_db', default=None)
request_user_id: ContextVar[Optional[str]] = ContextVar('request_user_id', default=None)


def set_request_context(db: AsyncSession, user_id: str) -> None:
    """
    设置当前请求的上下文

    应在API端点的开始处调用，设置后会自动传播到所有嵌套的异步函数调用中。

    Args:
        db: 当前请求的数据库会话
        user_id: 当前请求的用户ID

    Example:
        @router.post("/chat")
        async def agent_chat(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_active_user)
        ):
            set_request_context(db, str(current_user.id))
            # ... 后续所有调用都能自动获取 db 和 user_id
    """
    request_db.set(db)
    request_user_id.set(user_id)
    logger.debug(f"[RequestContext] 设置请求上下文: user_id={user_id}")


def get_request_db() -> Optional[AsyncSession]:
    """
    获取当前请求的数据库会话

    Returns:
        当前请求的数据库会话，如果未设置则返回 None
    """
    return request_db.get()


def get_request_user_id() -> Optional[str]:
    """
    获取当前请求的用户ID

    Returns:
        当前请求的用户ID，如果未设置则返回 None
    """
    return request_user_id.get()


def clear_request_context() -> None:
    """
    清理请求上下文

    注意：通常不需要手动调用，contextvars 会在请求结束时自动清理。
    此函数主要用于测试或特殊场景。
    """
    request_db.set(None)
    request_user_id.set(None)
    logger.debug("[RequestContext] 清理请求上下文")


def get_context_info() -> dict:
    """
    获取当前上下文信息（用于调试）

    Returns:
        包含上下文状态的字典
    """
    db = get_request_db()
    user_id = get_request_user_id()
    return {
        "has_db": db is not None,
        "user_id": user_id,
        "db_type": type(db).__name__ if db else None
    }
