"""
追踪中间件

为每个请求生成和传递trace_id，用于分布式追踪和日志关联
"""

import uuid
from contextvars import ContextVar
from typing import Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# 全局trace_id context变量
trace_context: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)


def get_trace_id() -> Optional[str]:
    """获取当前trace_id"""
    return trace_context.get(None)


class TraceMiddleware(BaseHTTPMiddleware):
    """追踪中间件 - 为每个请求生成和传递trace_id"""

    async def dispatch(self, request: Request, call_next):
        """
        处理请求，生成或提取trace_id

        Args:
            request: FastAPI请求对象
            call_next: 下一个中间件或路由处理器

        Returns:
            响应对象，添加了X-Trace-ID头
        """
        # 1. 生成或提取trace_id
        # 优先级：请求头 > 生成新ID
        trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())

        # 2. 设置到context（供日志使用）
        trace_context.set(trace_id)

        # 3. 添加到request state（供业务代码使用）
        request.state.trace_id = trace_id

        try:
            # 4. 处理请求
            response = await call_next(request)

            # 5. 添加trace_id到响应头
            response.headers["X-Trace-ID"] = trace_id

            return response

        finally:
            # 6. 清理context
            trace_context.set(None)
