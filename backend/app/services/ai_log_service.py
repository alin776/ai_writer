"""
AI调用日志服务

提供AI调用日志的创建、查询和统计功能
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, and_, extract, select
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta, timezone
from uuid import UUID
import uuid as uuid_lib

from app.models.ai_call_log import AICallLog
from app.schemas.ai_call_log import (
    AICallLogCreate,
    AICallLogStats,
    CostMetrics
)


class AILogService:
    """AI日志服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ==================== 新增: 便捷日志方法 ====================

    async def log_ai_call_start(
        self,
        user_id: UUID,
        operation: str,
        prompt_text: str,
        model_name: str
    ) -> UUID:
        """
        记录 AI 调用开始

        Args:
            user_id: 用户ID
            operation: 操作类型 (如 "chapter_review", "task_generation")
            prompt_text: 提示词
            model_name: 模型名称

        Returns:
            UUID: 日志ID
        """
        log_id = uuid_lib.uuid4()
        log = AICallLog(
            id=log_id,
            user_id=user_id,
            operation_type=operation,
            model_name=model_name,
            is_success=False,  # 初始为失败,成功时更新
            extra_data={"prompt_preview": prompt_text[:500]}  # 存储提示词预览到 extra_data
            # created_at 会自动使用 server_default
        )
        self.db.add(log)
        await self.db.flush()  # 立即写入,获取ID
        return log_id

    async def log_ai_call_success(
        self,
        log_id: UUID,
        response_text: str,
        prompt_tokens: int,
        completion_tokens: int
    ):
        """
        记录 AI 调用成功

        Args:
            log_id: 日志ID
            response_text: AI 响应文本
            prompt_tokens: 输入token数
            completion_tokens: 输出token数
        """
        result = await self.db.execute(
            select(AICallLog).where(AICallLog.id == log_id)
        )
        log = result.scalar_one_or_none()

        if log:
            log.is_success = True
            log.prompt_tokens = prompt_tokens
            log.completion_tokens = completion_tokens
            log.total_tokens = prompt_tokens + completion_tokens

            # 使用 CostCalculator 计算真实成本
            from app.utils.cost_calculator import CostCalculator

            cost_data = CostCalculator.calculate_cost(
                model_name=log.model_name,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )

            log.prompt_cost = cost_data["prompt_cost"]
            log.completion_cost = cost_data["completion_cost"]
            log.total_cost = cost_data["total_cost"]

            # 存储响应预览到 extra_data
            if log.extra_data:
                log.extra_data["response_preview"] = response_text[:500]
            else:
                log.extra_data = {"response_preview": response_text[:500]}

            # 计算耗时
            if log.created_at:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                duration = (now - log.created_at).total_seconds() * 1000
                log.duration_ms = int(duration)

            await self.db.commit()

    async def log_ai_call_error(
        self,
        log_id: UUID,
        error_message: str
    ):
        """
        记录 AI 调用失败

        Args:
            log_id: 日志ID
            error_message: 错误信息
        """
        result = await self.db.execute(
            select(AICallLog).where(AICallLog.id == log_id)
        )
        log = result.scalar_one_or_none()

        if log:
            log.is_success = False
            log.error_message = error_message[:1000]  # 限制长度

            # 计算耗时
            if log.created_at:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                duration = (now - log.created_at).total_seconds() * 1000
                log.duration_ms = int(duration)

            await self.db.commit()

    # ==================== 原有方法 ====================

    async def create_log(
        self,
        log_data: AICallLogCreate,
        auto_commit: bool = True  # ✅ 2025-12-14: 支持外层事务控制
    ) -> AICallLog:
        """
        创建AI调用日志

        Args:
            log_data: 日志数据
            auto_commit: 是否自动提交（默认True）。设为False时由外层控制事务

        Returns:
            AICallLog: 创建的日志记录
        """
        log = AICallLog(**log_data.model_dump())
        self.db.add(log)

        # ✅ 2025-12-14: 支持外层事务控制
        if auto_commit:
            await self.db.commit()
            await self.db.refresh(log)
        else:
            # 仅 flush 获取 ID，不提交事务
            await self.db.flush()

        return log

    async def get_user_logs(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AICallLog]:
        """
        获取用户的AI调用日志

        Args:
            user_id: 用户ID
            skip: 跳过记录数
            limit: 限制返回数量
            start_date: 起始时间
            end_date: 结束时间

        Returns:
            List[AICallLog]: 日志列表
        """
        stmt = select(AICallLog).where(AICallLog.user_id == user_id)

        if start_date:
            stmt = stmt.where(AICallLog.created_at >= start_date)
        if end_date:
            stmt = stmt.where(AICallLog.created_at <= end_date)

        stmt = stmt.order_by(AICallLog.created_at.desc()).offset(skip).limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_user_logs_count(
        self,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        """
        获取用户AI调用日志总数

        Args:
            user_id: 用户ID
            start_date: 起始时间
            end_date: 结束时间

        Returns:
            int: 日志总数
        """
        stmt = select(func.count(AICallLog.id)).where(AICallLog.user_id == user_id)

        if start_date:
            stmt = stmt.where(AICallLog.created_at >= start_date)
        if end_date:
            stmt = stmt.where(AICallLog.created_at <= end_date)

        result = await self.db.scalar(stmt)
        return result or 0

    async def get_stats(
        self,
        user_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> AICallLogStats:
        """
        获取AI调用统计数据

        Args:
            user_id: 用户ID(可选,不传则统计所有用户)
            start_date: 起始时间
            end_date: 结束时间

        Returns:
            AICallLogStats: 统计数据
        """
        # 构建基础查询条件
        conditions = []
        if user_id:
            conditions.append(AICallLog.user_id == user_id)
        if start_date:
            conditions.append(AICallLog.created_at >= start_date)
        if end_date:
            conditions.append(AICallLog.created_at <= end_date)

        # 总体统计 - 总调用次数
        total_calls_stmt = select(func.count(AICallLog.id))
        if conditions:
            total_calls_stmt = total_calls_stmt.where(and_(*conditions))
        total_calls = await self.db.scalar(total_calls_stmt) or 0

        if total_calls == 0:
            return AICallLogStats(
                total_calls=0,
                total_tokens=0,
                total_cost=0.0,
                success_rate=0.0,
                avg_duration_ms=None,
                by_model={},
                by_operation={},
                start_date=start_date,
                end_date=end_date
            )

        # 总 tokens
        total_tokens_stmt = select(func.sum(AICallLog.total_tokens))
        if conditions:
            total_tokens_stmt = total_tokens_stmt.where(and_(*conditions))
        total_tokens = await self.db.scalar(total_tokens_stmt) or 0

        # 总成本
        total_cost_stmt = select(func.sum(AICallLog.total_cost))
        if conditions:
            total_cost_stmt = total_cost_stmt.where(and_(*conditions))
        total_cost = await self.db.scalar(total_cost_stmt) or 0.0

        # 成功次数
        success_conditions = conditions + [AICallLog.is_success == True]
        success_count_stmt = select(func.count(AICallLog.id)).where(and_(*success_conditions))
        success_count = await self.db.scalar(success_count_stmt) or 0
        success_rate = (success_count / total_calls * 100) if total_calls > 0 else 0.0

        # 平均耗时
        avg_duration_conditions = conditions + [AICallLog.duration_ms.isnot(None)]
        avg_duration_stmt = select(func.avg(AICallLog.duration_ms)).where(and_(*avg_duration_conditions))
        avg_duration = await self.db.scalar(avg_duration_stmt)

        # 按模型统计
        by_model = {}
        model_stats_stmt = select(
            AICallLog.model_name,
            func.count(AICallLog.id).label('calls'),
            func.sum(AICallLog.total_tokens).label('tokens'),
            func.sum(AICallLog.total_cost).label('cost')
        )
        if conditions:
            model_stats_stmt = model_stats_stmt.where(and_(*conditions))
        model_stats_stmt = model_stats_stmt.group_by(AICallLog.model_name)

        result = await self.db.execute(model_stats_stmt)
        model_stats = result.all()

        for stat in model_stats:
            by_model[stat.model_name] = {
                'calls': stat.calls,
                'tokens': stat.tokens or 0,
                'cost': float(stat.cost) if stat.cost else 0.0
            }

        # 按操作类型统计
        by_operation = {}
        operation_stats_stmt = select(
            AICallLog.operation_type,
            func.count(AICallLog.id).label('calls'),
            func.sum(AICallLog.total_tokens).label('tokens'),
            func.sum(AICallLog.total_cost).label('cost')
        )
        if conditions:
            operation_stats_stmt = operation_stats_stmt.where(and_(*conditions))
        operation_stats_stmt = operation_stats_stmt.group_by(AICallLog.operation_type)

        result = await self.db.execute(operation_stats_stmt)
        operation_stats = result.all()

        for stat in operation_stats:
            by_operation[stat.operation_type] = {
                'calls': stat.calls,
                'tokens': stat.tokens or 0,
                'cost': float(stat.cost) if stat.cost else 0.0
            }

        return AICallLogStats(
            total_calls=total_calls,
            total_tokens=int(total_tokens),
            total_cost=float(total_cost),
            success_rate=round(success_rate, 2),
            avg_duration_ms=float(avg_duration) if avg_duration else None,
            by_model=by_model,
            by_operation=by_operation,
            start_date=start_date,
            end_date=end_date
        )

    async def get_cost_metrics(self) -> CostMetrics:
        """
        获取成本指标(用于管理后台)

        Returns:
            CostMetrics: 成本指标数据
        """
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)

        # 本月第一天
        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # 上月第一天
        if now.month == 1:
            last_month_start = now.replace(year=now.year - 1, month=12, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            last_month_start = now.replace(month=now.month - 1, day=1, hour=0, minute=0, second=0, microsecond=0)

        # 今日成本
        today_cost_stmt = select(func.sum(AICallLog.total_cost)).where(
            AICallLog.created_at >= today_start
        )
        today_cost = await self.db.scalar(today_cost_stmt) or 0.0

        # 昨日成本
        yesterday_cost_stmt = select(func.sum(AICallLog.total_cost)).where(
            and_(
                AICallLog.created_at >= yesterday_start,
                AICallLog.created_at < today_start
            )
        )
        yesterday_cost = await self.db.scalar(yesterday_cost_stmt) or 0.0

        # 本月成本
        this_month_cost_stmt = select(func.sum(AICallLog.total_cost)).where(
            AICallLog.created_at >= this_month_start
        )
        this_month_cost = await self.db.scalar(this_month_cost_stmt) or 0.0

        # 上月成本
        last_month_cost_stmt = select(func.sum(AICallLog.total_cost)).where(
            and_(
                AICallLog.created_at >= last_month_start,
                AICallLog.created_at < this_month_start
            )
        )
        last_month_cost = await self.db.scalar(last_month_cost_stmt) or 0.0

        # 今日调用次数
        today_calls_stmt = select(func.count(AICallLog.id)).where(
            AICallLog.created_at >= today_start
        )
        today_calls = await self.db.scalar(today_calls_stmt) or 0

        # 本月调用次数
        this_month_calls_stmt = select(func.count(AICallLog.id)).where(
            AICallLog.created_at >= this_month_start
        )
        this_month_calls = await self.db.scalar(this_month_calls_stmt) or 0

        # 最近7天成本趋势
        daily_costs = []
        for i in range(6, -1, -1):
            day_start = today_start - timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            day_cost_stmt = select(func.sum(AICallLog.total_cost)).where(
                and_(
                    AICallLog.created_at >= day_start,
                    AICallLog.created_at < day_end
                )
            )
            day_cost = await self.db.scalar(day_cost_stmt) or 0.0
            daily_costs.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'cost': float(day_cost)
            })

        # Top 5 用户
        top_users_stmt = select(
            AICallLog.user_id,
            func.sum(AICallLog.total_cost).label('total_cost'),
            func.count(AICallLog.id).label('total_calls'),
            func.sum(AICallLog.prompt_tokens).label('total_input_tokens'),
            func.sum(AICallLog.completion_tokens).label('total_output_tokens'),
            func.sum(AICallLog.cache_read_tokens).label('total_cache_read'),
            func.sum(AICallLog.cache_creation_tokens).label('total_cache_creation'),
            func.sum(AICallLog.reasoning_tokens).label('total_reasoning'),
        ).where(
            AICallLog.created_at >= this_month_start
        ).group_by(AICallLog.user_id).order_by(
            func.sum(AICallLog.total_cost).desc()
        ).limit(5)

        result = await self.db.execute(top_users_stmt)
        top_users_data = result.all()

        top_users = [
            {
                'user_id': str(user.user_id),
                'total_cost': float(user.total_cost),
                'total_calls': user.total_calls,
                'total_input_tokens': int(user.total_input_tokens or 0),
                'total_output_tokens': int(user.total_output_tokens or 0),
                'total_cache_read': int(user.total_cache_read or 0),
                'total_cache_creation': int(user.total_cache_creation or 0),
                'total_reasoning': int(user.total_reasoning or 0),
            }
            for user in top_users_data
        ]

        # Top 5 模型
        top_models_stmt = select(
            AICallLog.model_name,
            func.sum(AICallLog.total_cost).label('total_cost'),
            func.count(AICallLog.id).label('total_calls'),
            func.sum(AICallLog.prompt_tokens).label('total_input_tokens'),
            func.sum(AICallLog.completion_tokens).label('total_output_tokens'),
            func.sum(AICallLog.cache_read_tokens).label('total_cache_read'),
            func.sum(AICallLog.cache_creation_tokens).label('total_cache_creation'),
            func.sum(AICallLog.reasoning_tokens).label('total_reasoning'),
        ).where(
            AICallLog.created_at >= this_month_start
        ).group_by(AICallLog.model_name).order_by(
            func.sum(AICallLog.total_cost).desc()
        ).limit(5)

        result = await self.db.execute(top_models_stmt)
        top_models_data = result.all()

        top_models = [
            {
                'model_name': model.model_name,
                'total_cost': float(model.total_cost),
                'total_calls': model.total_calls,
                'total_input_tokens': int(model.total_input_tokens or 0),
                'total_output_tokens': int(model.total_output_tokens or 0),
                'total_cache_read': int(model.total_cache_read or 0),
                'total_cache_creation': int(model.total_cache_creation or 0),
                'total_reasoning': int(model.total_reasoning or 0),
            }
            for model in top_models_data
        ]

        return CostMetrics(
            today_cost=float(today_cost),
            yesterday_cost=float(yesterday_cost),
            this_month_cost=float(this_month_cost),
            last_month_cost=float(last_month_cost),
            today_calls=today_calls,
            this_month_calls=this_month_calls,
            daily_costs=daily_costs,
            top_users=top_users,
            top_models=top_models
        )
