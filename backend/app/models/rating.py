from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class WorkRating(Base):
    """作品评分模型 - 用户对整部作品的评分"""

    __tablename__ = "work_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)

    # 评分 1-5星
    rating = Column(Integer, nullable=False, comment="评分(1-5)")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", backref="work_ratings")
    work = relationship("Work", backref="work_ratings")

    # 唯一约束:每个用户对每部作品只能评分一次
    __table_args__ = (
        UniqueConstraint('user_id', 'work_id', name='uq_user_work_rating'),
    )

    def __repr__(self):
        return f"<WorkRating user_id={self.user_id} work_id={self.work_id} rating={self.rating}>"
