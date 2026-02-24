from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Bookshelf(Base):
    """书架模型 - 用户收藏的作品"""

    __tablename__ = "bookshelves"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)

    # 阅读进度 - 记录用户读到哪一章
    last_read_chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="SET NULL"), nullable=True)
    last_read_chapter_num = Column(Integer, nullable=True, comment="最后阅读的章节序号（FS 迁移后使用）")
    last_read_position = Column(Integer, default=0, nullable=False, comment="阅读位置(字符偏移量)")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="加入书架时间")
    last_read_at = Column(DateTime(timezone=True), nullable=True, comment="最后阅读时间")

    # 关联关系
    user = relationship("User", backref="bookshelf_items")
    work = relationship("Work", back_populates="bookshelf_items")
    last_read_chapter = relationship("Chapter", foreign_keys=[last_read_chapter_id])

    def __repr__(self):
        return f"<Bookshelf user_id={self.user_id} work_id={self.work_id}>"
