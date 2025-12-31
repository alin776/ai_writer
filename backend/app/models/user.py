from sqlalchemy import Column, String, DateTime, Boolean, Text, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class User(Base):
    """用户模型"""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    # 用户信息
    full_name = Column(String(100), nullable=True)
    avatar = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    honor = Column(String(50), nullable=True)  # 用户称号
    notification_settings = Column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb")
    )
    preferences = Column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb")
    )
    
    # 状态
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    works = relationship("Work", back_populates="author", cascade="all, delete-orphan")
    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    knowledge_items = relationship("KnowledgeItem", back_populates="user", cascade="all, delete-orphan")
    user_tasks = relationship("UserTask", back_populates="user", cascade="all, delete-orphan")
    created_channels = relationship("Channel", foreign_keys="Channel.creator_id", back_populates="creator", cascade="all, delete-orphan")
    channel_memberships = relationship("ChannelMember", back_populates="user", cascade="all, delete-orphan")
    channel_messages = relationship("ChannelMessage", foreign_keys="ChannelMessage.user_id", back_populates="user", cascade="all, delete-orphan")
    message_reactions = relationship("MessageReaction", back_populates="user", cascade="all, delete-orphan")
    message_attachments = relationship("MessageAttachment", back_populates="user", cascade="all, delete-orphan")
    channel_invites = relationship("ChannelInvite", back_populates="creator", cascade="all, delete-orphan")
    message_bookmarks = relationship("MessageBookmark", back_populates="user", cascade="all, delete-orphan")
    channel_notification_settings = relationship("ChannelNotificationSetting", back_populates="user", cascade="all, delete-orphan")
    stickers = relationship("UserSticker", back_populates="user", cascade="all, delete-orphan")
    favorite_stickers = relationship("UserFavoriteSticker", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"
