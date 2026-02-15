"""
小说举报 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.work_report import WorkReportReason, WorkReportStatus


class WorkReportCreate(BaseModel):
    """创建小说举报"""
    reason: WorkReportReason
    description: Optional[str] = Field(None, max_length=500, description="详细描述")


class WorkReportResponse(BaseModel):
    """小说举报响应"""
    id: UUID
    work_id: UUID
    reporter_id: UUID
    reason: WorkReportReason
    description: Optional[str] = None
    status: WorkReportStatus
    action_taken: Optional[str] = None
    admin_note: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
class WorkReportListResponse(BaseModel):
    """小说举报列表响应"""
    total: int
    items: list[WorkReportResponse]


# ==================== 管理员处理相关 Schema ====================

class ReportProcessRequest(BaseModel):
    """处理举报请求"""
    action: str = Field(..., description="处理操作: dismiss, warn, delete, ban")
    admin_note: Optional[str] = Field(None, max_length=500, description="管理员备注")


class MessageReportAdminResponse(BaseModel):
    """消息举报管理响应（包含关联信息）"""
    id: UUID
    message_id: UUID
    reporter_id: UUID
    reason: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[UUID] = None
    # 关联信息
    message_content: Optional[str] = None
    channel_name: Optional[str] = None
    reporter_name: Optional[str] = None
    reported_user_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
class CommentReportAdminResponse(BaseModel):
    """评论举报管理响应（包含关联信息）"""
    id: UUID
    comment_id: UUID
    user_id: UUID
    reason: str
    description: Optional[str] = None
    is_processed: bool
    processed_at: Optional[datetime] = None
    processed_by: Optional[UUID] = None
    created_at: datetime
    # 关联信息
    comment_content: Optional[str] = None
    work_title: Optional[str] = None
    reporter_name: Optional[str] = None
    commented_user_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
class WorkReportAdminResponse(BaseModel):
    """小说举报管理响应（包含关联信息）"""
    id: UUID
    work_id: UUID
    reporter_id: UUID
    reason: WorkReportReason
    description: Optional[str] = None
    status: WorkReportStatus
    action_taken: Optional[str] = None
    admin_note: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[UUID] = None
    created_at: datetime
    # 关联信息
    work_title: Optional[str] = None
    work_author_name: Optional[str] = None
    reporter_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
class UserReportAdminResponse(BaseModel):
    """用户举报管理响应（包含关联信息）"""
    id: UUID
    reporter_id: UUID
    reported_user_id: UUID
    reason: str
    description: Optional[str] = None
    status: str
    admin_note: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[UUID] = None
    created_at: datetime
    # 关联信息
    reporter_name: Optional[str] = None
    reported_user_name: Optional[str] = None
    reported_user_avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
class ReportSummary(BaseModel):
    """举报统计概览"""
    message_reports: dict  # { total, pending, processed_today }
    comment_reports: dict
    work_reports: dict
    user_reports: Optional[dict] = None  # { total, pending, processed_today }
