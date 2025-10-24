"""
AI调用日志 Schema

用于API请求和响应的数据验证
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class AICallLogBase(BaseModel):
    """AI调用日志基础Schema"""
    model_name: str = Field(..., description="AI模型名称")
    operation_type: str = Field(..., description="操作类型")
    work_id: Optional[UUID] = Field(None, description="关联作品ID")
    chapter_id: Optional[UUID] = Field(None, description="关联章节ID")
    analysis_id: Optional[UUID] = Field(None, description="关联分析ID")
    prompt_tokens: int = Field(0, description="提示词token数")
    completion_tokens: int = Field(0, description="生成内容token数")
    total_tokens: int = Field(0, description="总token数")
    prompt_cost: float = Field(0.0, description="提示词成本(美元)")
    completion_cost: float = Field(0.0, description="生成内容成本(美元)")
    total_cost: float = Field(0.0, description="总成本(美元)")
    duration_ms: Optional[int] = Field(None, description="调用耗时(毫秒)")
    is_success: bool = Field(True, description="是否成功")
    error_message: Optional[str] = Field(None, description="错误信息")
    extra_data: Dict[str, Any] = Field(default_factory=dict, description="额外数据")


class AICallLogCreate(AICallLogBase):
    """创建AI调用日志"""
    user_id: UUID = Field(..., description="用户ID")


class AICallLogResponse(AICallLogBase):
    """AI调用日志响应"""
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AICallLogStats(BaseModel):
    """AI调用统计"""
    total_calls: int = Field(..., description="总调用次数")
    total_tokens: int = Field(..., description="总token数")
    total_cost: float = Field(..., description="总成本(美元)")
    success_rate: float = Field(..., description="成功率(%)")
    avg_duration_ms: Optional[float] = Field(None, description="平均耗时(毫秒)")

    # 按模型统计
    by_model: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="按模型分组的统计数据"
    )

    # 按操作类型统计
    by_operation: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="按操作类型分组的统计数据"
    )

    # 时间范围
    start_date: Optional[datetime] = Field(None, description="统计起始时间")
    end_date: Optional[datetime] = Field(None, description="统计结束时间")

    model_config = ConfigDict(from_attributes=True)


class CostMetrics(BaseModel):
    """成本指标 (用于前端管理后台)"""
    today_cost: float = Field(..., description="今日成本")
    yesterday_cost: float = Field(..., description="昨日成本")
    this_month_cost: float = Field(..., description="本月成本")
    last_month_cost: float = Field(..., description="上月成本")

    today_calls: int = Field(..., description="今日调用次数")
    this_month_calls: int = Field(..., description="本月调用次数")

    # 成本趋势 (最近7天)
    daily_costs: list[Dict[str, Any]] = Field(
        default_factory=list,
        description="每日成本趋势"
    )

    # Top 用户
    top_users: list[Dict[str, Any]] = Field(
        default_factory=list,
        description="成本最高的用户"
    )

    # Top 模型
    top_models: list[Dict[str, Any]] = Field(
        default_factory=list,
        description="使用最多的模型"
    )

    model_config = ConfigDict(from_attributes=True)
