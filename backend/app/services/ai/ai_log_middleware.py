"""
AI日志记录中间件

为AI服务调用自动记录日志和计算成本
"""

import time
import logging
from typing import Optional, Dict, Any
from uuid import UUID
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session
from app.schemas.ai_call_log import AICallLogCreate
from app.services.ai_log_service import AILogService
from app.utils.cost_calculator import CostCalculator

logger = logging.getLogger(__name__)


class AILogMiddleware:
    """AI日志记录中间件"""

    def __init__(
        self,
        db: Session,
        user_id: UUID,
        model_name: str
    ):
        """
        初始化日志中间件

        Args:
            db: 数据库会话
            user_id: 用户ID
            model_name: 模型名称
        """
        self.db = db
        self.user_id = user_id
        self.model_name = model_name
        self.log_service = AILogService(db)

    @asynccontextmanager
    async def log_call(
        self,
        operation_type: str,
        work_id: Optional[UUID] = None,
        chapter_id: Optional[UUID] = None,
        analysis_id: Optional[UUID] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ):
        """
        记录AI调用的上下文管理器

        Args:
            operation_type: 操作类型
            work_id: 作品ID
            chapter_id: 章节ID
            analysis_id: 分析ID
            extra_data: 额外元数据

        Yields:
            TokenCounter: Token计数器对象，用于累积token数
        """
        start_time = time.time()
        token_counter = TokenCounter()
        is_success = True
        error_message = None

        try:
            yield token_counter
        except Exception as e:
            is_success = False
            error_message = str(e)
            raise
        finally:
            # 计算耗时
            duration_ms = int((time.time() - start_time) * 1000)

            # 计算成本
            cost_data = CostCalculator.calculate_cost(
                model_name=self.model_name,
                prompt_tokens=token_counter.prompt_tokens,
                completion_tokens=token_counter.completion_tokens
            )

            # 创建日志记录
            try:
                log_data = AICallLogCreate(
                    user_id=self.user_id,
                    model_name=self.model_name,
                    operation_type=operation_type,
                    work_id=work_id,
                    chapter_id=chapter_id,
                    analysis_id=analysis_id,
                    prompt_tokens=token_counter.prompt_tokens,
                    completion_tokens=token_counter.completion_tokens,
                    total_tokens=token_counter.total_tokens,
                    prompt_cost=cost_data["prompt_cost"],
                    completion_cost=cost_data["completion_cost"],
                    total_cost=cost_data["total_cost"],
                    duration_ms=duration_ms,
                    is_success=is_success,
                    error_message=error_message,
                    extra_data=extra_data or {}
                )

                self.log_service.create_log(log_data)

                logger.info(
                    f"AI调用日志已记录: operation={operation_type}, "
                    f"tokens={token_counter.total_tokens}, "
                    f"cost=${cost_data['total_cost']:.6f}, "
                    f"duration={duration_ms}ms, "
                    f"success={is_success}"
                )
            except Exception as log_error:
                # 日志记录失败不应影响主流程
                logger.error(f"AI日志记录失败: {log_error}", exc_info=True)


class TokenCounter:
    """Token计数器"""

    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def set_tokens(self, prompt_tokens: int, completion_tokens: int):
        """设置token数量"""
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens

    def add_completion_tokens(self, tokens: int):
        """累加生成token数"""
        self.completion_tokens += tokens

    def estimate_tokens(self, text: str) -> int:
        """
        估算文本的token数量

        简单估算: 1个token ≈ 4个字符（英文）或 1.5个中文字符
        """
        # 统计中英文字符
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        other_chars = len(text) - chinese_chars

        # 估算token
        estimated = int(chinese_chars / 1.5 + other_chars / 4)
        return max(1, estimated)  # 至少1个token
