from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class ChapterWordStat(Base):
    """章节字数增量统计表（按事件记录 delta，仅记录正增量）"""

    __tablename__ = "chapter_word_stats"
    # 注意：幂等性约束使用部分唯一索引（在迁移脚本中创建）
    # CREATE UNIQUE INDEX ... WHERE edit_event_id IS NOT NULL

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    delta = Column(Integer, nullable=False, default=0)
    # 编辑事件唯一标识，用于幂等性检查
    edit_event_id = Column(String(64), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    def __repr__(self):
        return f"<ChapterWordStat chapter_id={self.chapter_id} delta={self.delta} edit_event_id={self.edit_event_id}>"
