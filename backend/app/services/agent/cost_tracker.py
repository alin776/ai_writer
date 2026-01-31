# ================================
# ⚠️ DEPRECATED - 2025-12-01
# ================================
# 本文件已弃用，请使用 AILogService 替代
# 保留此文件仅用于紧急回滚
# 计划删除日期：验证AILogService稳定运行1个月后（2026-01-01）
#
# 新的成本追踪方案：
# - 数据模型：backend/app/models/ai_call_log.py
# - 服务层：backend/app/services/ai_log_service.py
# - API接口：backend/app/api/ai_logs.py
# ================================

"""
⚠️ DEPRECATED - 成本追踪系统 - Week 7

警告：此模块已被弃用，请使用 AILogService 替代

原因：
1. CostTracker使用内存存储，应用重启后数据丢失
2. 存在内存泄漏问题（_records无限增长）
3. AICallLog提供数据库持久化，支持复杂查询和积分系统对接

迁移指南：
- 旧代码：tracker = get_cost_tracker()
- 新代码：log_service = AILogService(db)

相关文档：
- 迁移执行计划：AI成本追踪系统-迁移执行计划.md
- 审计报告：AI成本追踪系统审计报告.md

---
原功能说明（已弃用）：

追踪和分析 AI API 调用成本
参考: novel-ai-agent-Chinese 的成本优化策略

核心功能:
1. API 调用成本追踪
2. 用户成本统计
3. 成本报告生成
4. 成本预警和限额
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from collections import defaultdict
import logging
import json
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


# ==================== 数据模型 ====================

class APICallRecord(BaseModel):
    """API 调用记录"""
    id: str = Field(..., description="记录ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="调用时间")
    user_id: Optional[str] = Field(None, description="用户ID")
    work_id: Optional[str] = Field(None, description="作品ID")
    chapter_id: Optional[str] = Field(None, description="章节ID")

    # 模型信息
    model_provider: str = Field(..., description="模型提供商")
    model_id: str = Field(..., description="模型ID")
    model_name: str = Field(..., description="模型名称")

    # Token 使用
    input_tokens: int = Field(..., ge=0, description="输入token数")
    output_tokens: int = Field(..., ge=0, description="输出token数")
    total_tokens: int = Field(..., ge=0, description="总token数")

    # 成本信息
    input_cost: float = Field(..., ge=0, description="输入成本 (USD)")
    output_cost: float = Field(..., ge=0, description="输出成本 (USD)")
    total_cost: float = Field(..., ge=0, description="总成本 (USD)")

    # 任务信息
    task_type: Optional[str] = Field(None, description="任务类型")
    task_complexity: Optional[str] = Field(None, description="任务复杂度")

    # 性能信息
    response_time: Optional[float] = Field(None, description="响应时间 (秒)")
    success: bool = Field(default=True, description="是否成功")
    error_message: Optional[str] = Field(None, description="错误信息")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "call_123",
                "user_id": "user_001",
                "model_provider": "google",
                "model_id": "gemini-2.5-flash",
                "model_name": "Gemini 2.5 Flash",
                "input_tokens": 1000,
                "output_tokens": 500,
                "total_tokens": 1500,
                "input_cost": 0.0005,
                "output_cost": 0.00075,
                "total_cost": 0.00125,
                "task_type": "content_creation",
                "success": True
            }
        }


class CostStatistics(BaseModel):
    """成本统计"""
    period: str = Field(..., description="统计周期 (daily/weekly/monthly/all)")
    start_date: datetime = Field(..., description="开始日期")
    end_date: datetime = Field(..., description="结束日期")

    # 总体统计
    total_calls: int = Field(default=0, description="总调用次数")
    total_tokens: int = Field(default=0, description="总token数")
    total_cost: float = Field(default=0.0, description="总成本 (USD)")

    # 平均值
    avg_tokens_per_call: float = Field(default=0.0, description="平均每次调用token数")
    avg_cost_per_call: float = Field(default=0.0, description="平均每次调用成本 (USD)")

    # 按模型统计
    cost_by_model: Dict[str, float] = Field(
        default_factory=dict,
        description="按模型分组的成本"
    )
    calls_by_model: Dict[str, int] = Field(
        default_factory=dict,
        description="按模型分组的调用次数"
    )

    # 按任务类型统计
    cost_by_task_type: Dict[str, float] = Field(
        default_factory=dict,
        description="按任务类型分组的成本"
    )

    # 成功率
    success_rate: float = Field(default=0.0, ge=0, le=1, description="成功率 (0-1)")


# ==================== 成本追踪器 ====================

class CostTracker:
    """成本追踪器

    管理 API 调用成本的记录、统计和分析

    使用示例:
    ```python
    tracker = CostTracker()

    # 记录API调用
    await tracker.track_api_call(
        user_id="user_001",
        model_provider="google",
        model_id="gemini-2.5-flash",
        input_tokens=1000,
        output_tokens=500,
        input_cost=0.0003,
        output_cost=0.00125
    )

    # 获取统计
    stats = await tracker.get_cost_statistics(
        user_id="user_001",
        period="daily"
    )

    print(f"今日成本: ${stats.total_cost:.4f}")
    print(f"调用次数: {stats.total_calls}")
    ```
    """

    def __init__(self, enable_persistence: bool = False):
        """初始化成本追踪器

        Args:
            enable_persistence: 是否启用持久化 (存储到数据库)
        """
        self.enable_persistence = enable_persistence
        # 内存存储 (简化版,生产环境应使用数据库)
        self._records: List[APICallRecord] = []
        logger.info(f"CostTracker 初始化完成, 持久化: {enable_persistence}")

    async def track_api_call(
        self,
        user_id: Optional[str],
        model_provider: str,
        model_id: str,
        model_name: str,
        input_tokens: int,
        output_tokens: int,
        input_cost: float,
        output_cost: float,
        task_type: Optional[str] = None,
        task_complexity: Optional[str] = None,
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        response_time: Optional[float] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        db=None  # 新增：可选的AsyncSession用于持久化
    ) -> APICallRecord:
        """追踪单次 API 调用

        Args:
            user_id: 用户ID
            model_provider: 模型提供商
            model_id: 模型ID
            model_name: 模型名称
            input_tokens: 输入token数
            output_tokens: 输出token数
            input_cost: 输入成本 (USD)
            output_cost: 输出成本 (USD)
            task_type: 任务类型
            task_complexity: 任务复杂度
            work_id: 作品ID
            chapter_id: 章节ID
            response_time: 响应时间
            success: 是否成功
            error_message: 错误信息
            db: 可选的AsyncSession，用于持久化到数据库

        Returns:
            APICallRecord: API调用记录
        """
        # 生成记录ID
        record_id = f"call_{get_utc_now().strftime('%Y%m%d_%H%M%S_%f')}"

        # 创建记录
        record = APICallRecord(
            id=record_id,
            timestamp=get_utc_now(),
            user_id=user_id,
            work_id=work_id,
            chapter_id=chapter_id,
            model_provider=model_provider,
            model_id=model_id,
            model_name=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=input_cost + output_cost,
            task_type=task_type,
            task_complexity=task_complexity,
            response_time=response_time,
            success=success,
            error_message=error_message
        )

        # 存储记录
        self._records.append(record)

        logger.info(
            f"[CostTracker] 记录API调用: {model_name}, "
            f"tokens: {input_tokens}+{output_tokens}={input_tokens+output_tokens}, "
            f"cost: ${input_cost+output_cost:.6f}"
        )

        # 持久化 (如果启用)
        if self.enable_persistence:
            await self._persist_record(record, db=db)

        return record

    async def get_cost_statistics(
        self,
        user_id: Optional[str] = None,
        period: str = "all",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> CostStatistics:
        """获取成本统计

        Args:
            user_id: 用户ID (可选, 为None时统计所有用户)
            period: 统计周期 (daily/weekly/monthly/all)
            start_date: 开始日期 (可选)
            end_date: 结束日期 (可选)

        Returns:
            CostStatistics: 成本统计结果
        """
        # 确定日期范围
        if period == "daily":
            start_date = get_utc_now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = get_utc_now()
        elif period == "weekly":
            start_date = get_utc_now() - timedelta(days=7)
            end_date = get_utc_now()
        elif period == "monthly":
            start_date = get_utc_now() - timedelta(days=30)
            end_date = get_utc_now()
        elif period == "all":
            if not start_date:
                start_date = datetime.min
            if not end_date:
                end_date = get_utc_now()

        # 过滤记录
        filtered_records = [
            r for r in self._records
            if (not user_id or r.user_id == user_id)
            and start_date <= r.timestamp <= end_date
        ]

        if not filtered_records:
            return CostStatistics(
                period=period,
                start_date=start_date,
                end_date=end_date
            )

        # 计算统计
        total_calls = len(filtered_records)
        total_tokens = sum(r.total_tokens for r in filtered_records)
        total_cost = sum(r.total_cost for r in filtered_records)

        avg_tokens_per_call = total_tokens / total_calls if total_calls > 0 else 0
        avg_cost_per_call = total_cost / total_calls if total_calls > 0 else 0

        # 按模型统计
        cost_by_model = defaultdict(float)
        calls_by_model = defaultdict(int)
        for r in filtered_records:
            cost_by_model[r.model_id] += r.total_cost
            calls_by_model[r.model_id] += 1

        # 按任务类型统计
        cost_by_task_type = defaultdict(float)
        for r in filtered_records:
            if r.task_type:
                cost_by_task_type[r.task_type] += r.total_cost

        # 成功率
        success_count = sum(1 for r in filtered_records if r.success)
        success_rate = success_count / total_calls if total_calls > 0 else 0

        return CostStatistics(
            period=period,
            start_date=start_date,
            end_date=end_date,
            total_calls=total_calls,
            total_tokens=total_tokens,
            total_cost=total_cost,
            avg_tokens_per_call=avg_tokens_per_call,
            avg_cost_per_call=avg_cost_per_call,
            cost_by_model=dict(cost_by_model),
            calls_by_model=dict(calls_by_model),
            cost_by_task_type=dict(cost_by_task_type),
            success_rate=success_rate
        )

    async def check_cost_limit(
        self,
        user_id: str,
        period: str = "daily",
        limit: float = 1.0
    ) -> Dict[str, Any]:
        """检查成本限额

        Args:
            user_id: 用户ID
            period: 统计周期 (daily/weekly/monthly)
            limit: 成本限额 (USD)

        Returns:
            Dict: 检查结果
            {
                "within_limit": bool,
                "current_cost": float,
                "limit": float,
                "remaining": float,
                "usage_percentage": float
            }
        """
        stats = await self.get_cost_statistics(user_id=user_id, period=period)

        within_limit = stats.total_cost <= limit
        remaining = limit - stats.total_cost
        usage_percentage = (stats.total_cost / limit * 100) if limit > 0 else 0

        result = {
            "within_limit": within_limit,
            "current_cost": stats.total_cost,
            "limit": limit,
            "remaining": remaining,
            "usage_percentage": usage_percentage
        }

        if not within_limit:
            logger.warning(
                f"[CostTracker] 用户 {user_id} 超出{period}成本限额! "
                f"当前: ${stats.total_cost:.4f}, 限额: ${limit:.4f}"
            )

        return result

    async def get_cost_report(
        self,
        user_id: Optional[str] = None,
        period: str = "all"
    ) -> Dict[str, Any]:
        """生成成本报告

        Args:
            user_id: 用户ID (可选)
            period: 统计周期

        Returns:
            Dict: 详细的成本报告
        """
        stats = await self.get_cost_statistics(user_id=user_id, period=period)

        # 构建报告
        report = {
            "period": stats.period,
            "date_range": {
                "start": stats.start_date.isoformat(),
                "end": stats.end_date.isoformat()
            },
            "summary": {
                "total_calls": stats.total_calls,
                "total_tokens": stats.total_tokens,
                "total_cost": round(stats.total_cost, 4),
                "avg_tokens_per_call": round(stats.avg_tokens_per_call, 2),
                "avg_cost_per_call": round(stats.avg_cost_per_call, 6),
                "success_rate": round(stats.success_rate * 100, 2)
            },
            "breakdown": {
                "by_model": {
                    model: {
                        "cost": round(cost, 4),
                        "calls": stats.calls_by_model.get(model, 0),
                        "percentage": round(cost / stats.total_cost * 100, 2) if stats.total_cost > 0 else 0
                    }
                    for model, cost in stats.cost_by_model.items()
                },
                "by_task_type": {
                    task: {
                        "cost": round(cost, 4),
                        "percentage": round(cost / stats.total_cost * 100, 2) if stats.total_cost > 0 else 0
                    }
                    for task, cost in stats.cost_by_task_type.items()
                }
            }
        }

        return report

    async def _persist_record(self, record: APICallRecord, db=None):
        """持久化记录到数据库

        Args:
            record: API调用记录
            db: 可选的AsyncSession，如果提供则保存到数据库
        """
        if not self.enable_persistence or db is None:
            return

        try:
            from app.models.ai_call_log import AICallLog
            from uuid import UUID

            # 映射APICallRecord到AICallLog
            log_entry = AICallLog(
                user_id=UUID(record.user_id) if record.user_id else None,
                model_name=record.model_name,
                operation_type=record.task_type or "unknown",
                work_id=UUID(record.work_id) if record.work_id else None,
                chapter_id=UUID(record.chapter_id) if record.chapter_id else None,
                # Token统计
                prompt_tokens=record.input_tokens,
                completion_tokens=record.output_tokens,
                total_tokens=record.total_tokens,
                # 成本信息
                prompt_cost=record.input_cost,
                completion_cost=record.output_cost,
                total_cost=record.total_cost,
                # 性能信息
                duration_ms=int(record.response_time * 1000) if record.response_time else None,
                is_success=record.success,
                error_message=record.error_message,
                # 额外数据
                extra_data={
                    "model_provider": record.model_provider,
                    "model_id": record.model_id,
                    "task_complexity": record.task_complexity,
                    "timestamp": record.timestamp.isoformat()
                }
            )

            db.add(log_entry)
            await db.flush()  # 立即写入，但不提交事务

            logger.debug(f"[CostTracker] 记录已持久化到数据库: {record.id}")

        except Exception as e:
            logger.error(f"[CostTracker] 持久化记录失败: {type(e).__name__}: {e}")
            # 持久化失败不应影响主流程

    def get_recent_records(self, limit: int = 10) -> List[APICallRecord]:
        """获取最近的记录

        Args:
            limit: 返回记录数量

        Returns:
            List[APICallRecord]: 最近的记录列表
        """
        return sorted(
            self._records,
            key=lambda r: r.timestamp,
            reverse=True
        )[:limit]

    def export_records(
        self,
        file_path: str,
        format: str = "json"
    ):
        """导出记录到文件

        Args:
            file_path: 文件路径
            format: 导出格式 (json/csv)
        """
        if format == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                records_dict = [r.model_dump() for r in self._records]
                json.dump(records_dict, f, indent=2, default=str, ensure_ascii=False)
            logger.info(f"导出 {len(self._records)} 条记录到: {file_path}")
        elif format == "csv":
            # TODO: 实现CSV导出
            pass


# ==================== 全局实例 ====================

# 全局成本追踪器实例
_global_cost_tracker: Optional[CostTracker] = None


def get_cost_tracker() -> CostTracker:
    """获取全局成本追踪器实例"""
    global _global_cost_tracker
    if _global_cost_tracker is None:
        _global_cost_tracker = CostTracker()
    return _global_cost_tracker


# ==================== 导出 ====================

__all__ = [
    "APICallRecord",
    "CostStatistics",
    "CostTracker",
    "get_cost_tracker"
]
