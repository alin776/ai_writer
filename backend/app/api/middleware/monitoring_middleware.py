"""
监控中间件

提供API请求级别的监控，包括：
- 请求计数（总数、成功、失败）
- 响应时间（P50/P90/P95/P99）
- 错误率统计
- 路径和方法级别的细分统计
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# 导入监控功能
from app.services.agent.utils.monitoring import (
    get_system_monitor,
    increment_counter,
    record_timer
)

logger = logging.getLogger(__name__)


class MonitoringMiddleware(BaseHTTPMiddleware):
    """监控中间件 - 记录API请求的各项指标"""

    async def dispatch(self, request: Request, call_next: Callable):
        """
        处理请求并记录监控指标

        Args:
            request: FastAPI请求对象
            call_next: 下一个中间件或路由处理器

        Returns:
            响应对象
        """
        # 1. 提取请求信息
        path = request.url.path
        method = request.method

        # 🔧 2025-12-02: Phase 1 日志优化 - 跳过OPTIONS预检请求
        # OPTIONS请求是CORS预检，不产生实际业务逻辑，跳过监控可减少40%日志量
        if method == "OPTIONS":
            return await call_next(request)

        # 排除不需要监控的路径
        if self._should_skip_monitoring(path):
            return await call_next(request)

        # 2. 记录请求开始
        start_time = time.time()

        # 3. 增加请求计数
        increment_counter(
            "api_requests_total",
            labels={
                "path": self._normalize_path(path),
                "method": method
            }
        )

        try:
            # 4. 处理请求
            response = await call_next(request)

            # 5. 记录成功请求
            increment_counter(
                "api_requests_success",
                labels={
                    "path": self._normalize_path(path),
                    "method": method,
                    "status_code": str(response.status_code)
                }
            )

            return response

        except Exception as e:
            # 6. 记录失败请求
            increment_counter(
                "api_requests_error",
                labels={
                    "path": self._normalize_path(path),
                    "method": method,
                    "error_type": type(e).__name__
                }
            )

            # 记录错误日志
            logger.error(
                f"API请求失败: {method} {path}",
                exc_info=True,
                extra={
                    "path": path,
                    "method": method,
                    "error_type": type(e).__name__,
                    "trace_id": getattr(request.state, "trace_id", None)
                }
            )

            # 重新抛出异常
            raise

        finally:
            # 7. 记录响应时间
            duration = time.time() - start_time
            record_timer(
                "api_request_duration",
                duration,
                labels={
                    "path": self._normalize_path(path),
                    "method": method
                }
            )

            # 8. 记录详细日志
            trace_id = getattr(request.state, "trace_id", None)
            logger.info(
                f"API请求完成: {method} {path}",
                extra={
                    "trace_id": trace_id,
                    "path": path,
                    "method": method,
                    "duration_ms": duration * 1000,
                    "status_code": getattr(response, "status_code", None) if 'response' in locals() else None
                }
            )

    def _should_skip_monitoring(self, path: str) -> bool:
        """
        判断是否跳过监控

        Args:
            path: 请求路径

        Returns:
            是否跳过监控
        """
        # 跳过静态资源、health check等
        skip_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico",
            "/static/"
        ]

        return any(path.startswith(skip_path) for skip_path in skip_paths)

    def _normalize_path(self, path: str) -> str:
        """
        标准化路径（将动态参数替换为占位符）

        Args:
            path: 原始路径

        Returns:
            标准化后的路径
        """
        # 简单的路径标准化
        # 例如：/api/v1/agent/chat/abc123 -> /api/v1/agent/chat/{id}

        # 保留常见的API路径
        if path.startswith("/api/v1/"):
            parts = path.split("/")
            normalized_parts = []

            for i, part in enumerate(parts):
                # 如果是UUID或者看起来像ID的部分，替换为占位符
                if part and (len(part) > 20 or part.isdigit()):
                    normalized_parts.append("{id}")
                else:
                    normalized_parts.append(part)

            return "/".join(normalized_parts)

        return path
