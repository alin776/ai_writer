"""用户贴图模型"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class StickerSource(str, enum.Enum):
    """贴图来源"""
    UPLOAD = "upload"  # 用户上传
    TENOR = "tenor"    # 来自 Tenor


class UserSticker(Base):
    """用户自定义贴图模型"""

    __tablename__ = "user_stickers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 用户关联
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 贴图信息
    name = Column(String(100), nullable=True, comment="贴图名称")
    image_url = Column(String(500), nullable=False, comment="贴图图片URL")
    preview_url = Column(String(500), nullable=True, comment="预览图URL（小尺寸）")
    source = Column(SQLEnum(StickerSource), default=StickerSource.UPLOAD, nullable=False, comment="贴图来源")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", back_populates="stickers")

    def __repr__(self):
        return f"<UserSticker id={self.id} user_id={self.user_id}>"


class UserFavoriteSticker(Base):
    """用户收藏的贴图模型"""

    __tablename__ = "user_favorite_stickers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 用户关联
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 贴图信息
    sticker_url = Column(String(500), nullable=False, comment="贴图URL")
    preview_url = Column(String(500), nullable=True, comment="预览图URL")
    source = Column(SQLEnum(StickerSource), default=StickerSource.TENOR, nullable=False, comment="贴图来源")
    tenor_id = Column(String(100), nullable=True, comment="Tenor贴图ID（用于去重）")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", back_populates="favorite_stickers")

    def __repr__(self):
        return f"<UserFavoriteSticker id={self.id} user_id={self.user_id}>"
