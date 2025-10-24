"""
AI调用日志服务

提供AI调用日志的创建、查询和统计功能
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from uuid import UUID

from app.models.ai_call_log import AICallLog
from app.schemas.ai_call_log import (
    AICallLogCreate,
    AICallLogStats,
    CostMetrics
)


class AILogService:
    """AI日志服务"""

    def __init__(self, db: Session):
        self.db = db

    def create_log(self, log_data: AICallLogCreate) -> AICallLog:
        """
        创建AI调用日志

        Args:
            log_data: 日志数据

        Returns:
            AICallLog: 创建的日志记录
        """
        log = AICallLog(**log_data.model_dump())
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_user_logs(
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
        query = self.db.query(AICallLog).filter(AICallLog.user_id == user_id)

        if start_date:
            query = query.filter(AICallLog.created_at >= start_date)
        if end_date:
            query = query.filter(AICallLog.created_at <= end_date)

        return query.order_by(AICallLog.created_at.desc()).offset(skip).limit(limit).all()

    def get_stats(
        self,
        user_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> AICallLogStats:
        """
        获取AI调用统计数据

        Args:
            user_id: 用户ID（可选，不传则统计所有用户）
            start_date: 起始时间
            end_date: 结束时间

        Returns:
            AICallLogStats: 统计数据
        """
        query = self.db.query(AICallLog)

        if user_id:
            query = query.filter(AICallLog.user_id == user_id)
        if start_date:
            query = query.filter(AICallLog.created_at >= start_date)
        if end_date:
            query = query.filter(AICallLog.created_at <= end_date)

        # 总体统计
        total_calls = query.count()
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

        total_tokens = query.with_entities(func.sum(AICallLog.total_tokens)).scalar() or 0
        total_cost = query.with_entities(func.sum(AICallLog.total_cost)).scalar() or 0.0
        success_count = query.filter(AICallLog.is_success == True).count()
        success_rate = (success_count / total_calls * 100) if total_calls > 0 else 0.0

        avg_duration = query.filter(AICallLog.duration_ms.isnot(None)).with_entities(
            func.avg(AICallLog.duration_ms)
        ).scalar()

        # 按模型统计
        by_model = {}
        model_stats = self.db.query(
            AICallLog.model_name,
            func.count(AICallLog.id).label('calls'),
            func.sum(AICallLog.total_tokens).label('tokens'),
            func.sum(AICallLog.total_cost).label('cost')
        ).filter(
            and_(
                AICallLog.user_id == user_id if user_id else True,
                AICallLog.created_at >= start_date if start_date else True,
                AICallLog.created_at <= end_date if end_date else True
            )
        ).group_by(AICallLog.model_name).all()

        for stat in model_stats:
            by_model[stat.model_name] = {
                'calls': stat.calls,
                'tokens': stat.tokens or 0,
                'cost': float(stat.cost) if stat.cost else 0.0
            }

        # 按操作类型统计
        by_operation = {}
        operation_stats = self.db.query(
            AICallLog.operation_type,
            func.count(AICallLog.id).label('calls'),
            func.sum(AICallLog.total_tokens).label('tokens'),
            func.sum(AICallLog.total_cost).label('cost')
        ).filter(
            and_(
                AICallLog.user_id == user_id if user_id else True,
                AICallLog.created_at >= start_date if start_date else True,
                AICallLog.created_at <= end_date if end_date else True
            )
        ).group_by(AICallLog.operation_type).all()

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

    def get_cost_metrics(self) -> CostMetrics:
        """
        获取成本指标（用于管理后台）

        Returns:
            CostMetrics: 成本指标数据
        """
        now = datetime.utcnow()
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
        today_cost = self.db.query(func.sum(AICallLog.total_cost)).filter(
            AICallLog.created_at >= today_start
        ).scalar() or 0.0

        # 昨日成本
        yesterday_cost = self.db.query(func.sum(AICallLog.total_cost)).filter(
            and_(
                AICallLog.created_at >= yesterday_start,
                AICallLog.created_at < today_start
            )
        ).scalar() or 0.0

        # 本月成本
        this_month_cost = self.db.query(func.sum(AICallLog.total_cost)).filter(
            AICallLog.created_at >= this_month_start
        ).scalar() or 0.0

        # 上月成本
        last_month_cost = self.db.query(func.sum(AICallLog.total_cost)).filter(
            and_(
                AICallLog.created_at >= last_month_start,
                AICallLog.created_at < this_month_start
            )
        ).scalar() or 0.0

        # 今日调用次数
        today_calls = self.db.query(func.count(AICallLog.id)).filter(
            AICallLog.created_at >= today_start
        ).scalar() or 0

        # 本月调用次数
        this_month_calls = self.db.query(func.count(AICallLog.id)).filter(
            AICallLog.created_at >= this_month_start
        ).scalar() or 0

        # 最近7天成本趋势
        daily_costs = []
        for i in range(6, -1, -1):
            day_start = today_start - timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            day_cost = self.db.query(func.sum(AICallLog.total_cost)).filter(
                and_(
                    AICallLog.created_at >= day_start,
                    AICallLog.created_at < day_end
                )
            ).scalar() or 0.0
            daily_costs.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'cost': float(day_cost)
            })

        # Top 5 用户
        top_users_data = self.db.query(
            AICallLog.user_id,
            func.sum(AICallLog.total_cost).label('total_cost'),
            func.count(AICallLog.id).label('total_calls')
        ).filter(
            AICallLog.created_at >= this_month_start
        ).group_by(AICallLog.user_id).order_by(
            func.sum(AICallLog.total_cost).desc()
        ).limit(5).all()

        top_users = [
            {
                'user_id': str(user.user_id),
                'total_cost': float(user.total_cost),
                'total_calls': user.total_calls
            }
            for user in top_users_data
        ]

        # Top 5 模型
        top_models_data = self.db.query(
            AICallLog.model_name,
            func.sum(AICallLog.total_cost).label('total_cost'),
            func.count(AICallLog.id).label('total_calls')
        ).filter(
            AICallLog.created_at >= this_month_start
        ).group_by(AICallLog.model_name).order_by(
            func.sum(AICallLog.total_cost).desc()
        ).limit(5).all()

        top_models = [
            {
                'model_name': model.model_name,
                'total_cost': float(model.total_cost),
                'total_calls': model.total_calls
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
