from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.comment import ReportReason


class CommentReportCreate(BaseModel):
    """创建举报"""
    reason: ReportReason
    description: Optional[str] = Field(None, max_length=500, description="详细描述")


class CommentReportResponse(BaseModel):
    """举报响应"""
    id: UUID
    comment_id: UUID
    user_id: UUID
    reason: ReportReason
    description: Optional[str] = None
    is_processed: bool
    processed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
