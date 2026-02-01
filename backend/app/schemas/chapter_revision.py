from enum import Enum
from datetime import datetime
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, field_serializer, ConfigDict


class ChapterRevisionStatusEnum(str, Enum):
    """Revision status for API responses."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    DISCARDED = "discarded"
    CONFLICT = "conflict"


class ChapterRevisionResponse(BaseModel):
    """Chapter revision response."""

    id: UUID
    request_id: str
    work_id: UUID
    chapter_id: UUID
    status: ChapterRevisionStatusEnum
    operation: str
    original_text: Optional[str] = None
    new_text: str
    position: Optional[Any] = None
    before_anchor: Optional[str] = None
    after_anchor: Optional[str] = None
    node_id: Optional[str] = None
    paragraph_index: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    @field_serializer("id", "work_id", "chapter_id")
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)
