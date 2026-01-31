import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from app.core.database import Base


class AgentSessionMessage(Base):
  """
  Agent 会话消息表
  - 记录每条用户/Agent 消息
  """

  __tablename__ = "agent_session_messages"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  session_id = Column(UUID(as_uuid=True), ForeignKey("agent_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
  role = Column(String(20), nullable=False)  # user | agent
  content = Column(Text, nullable=False)
  message_metadata = Column('metadata', JSONB, nullable=True)
  token_usage = Column(JSONB, nullable=True)

  created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
