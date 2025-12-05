"""add agent_session_messages table

Revision ID: 9a6f9f4c0c1e
Revises: 4d7db5b2316c
Create Date: 2025-12-05 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9a6f9f4c0c1e'
down_revision = '4d7db5b2316c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'agent_session_messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('token_usage', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['agent_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_agent_session_messages_session_id', 'agent_session_messages', ['session_id'], unique=False)
    op.create_index('ix_agent_session_messages_created_at', 'agent_session_messages', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_agent_session_messages_created_at', table_name='agent_session_messages')
    op.drop_index('ix_agent_session_messages_session_id', table_name='agent_session_messages')
    op.drop_table('agent_session_messages')
