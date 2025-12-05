import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class AgentSession(Base):
  """
  Agent 会话表
  - 记录用户的 Agent 会话基础信息
  - 会话消息目前由上层流式接口管理，后续可扩展消息表
  """

  __tablename__ = "agent_sessions"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

  title = Column(String(200), nullable=True)
  conversation_id = Column(String(255), nullable=True, index=True)
  work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="SET NULL"), nullable=True, index=True)
  chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="SET NULL"), nullable=True, index=True)
  title_locked = Column(Boolean, nullable=True, default=False)

  created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
  archived_at = Column(DateTime(timezone=True), nullable=True)
  expires_at = Column(DateTime(timezone=True), nullable=True)
