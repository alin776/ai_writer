"""add_agent_session_message_index

Revision ID: add_agent_session_message_index
Revises: add_node_id_to_chapter_vectors
Create Date: 2026-01-30 00:01:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_agent_session_message_index"
down_revision = "add_node_id_to_chapter_vectors"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "ix_agent_session_messages_session_id_created_at",
        "agent_session_messages",
        ["session_id", "created_at"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_agent_session_messages_session_id_created_at", table_name="agent_session_messages")
