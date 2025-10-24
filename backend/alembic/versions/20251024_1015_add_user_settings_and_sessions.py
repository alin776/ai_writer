"""add user settings fields and sessions table

Revision ID: d1e2f3g4h5i6
Revises: c5d6e7f8g9h0
Create Date: 2025-10-24 10:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd1e2f3g4h5i6'
down_revision = 'c5d6e7f8g9h0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'notification_settings',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb")
        )
    )
    op.add_column(
        'users',
        sa.Column(
            'preferences',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb")
        )
    )

    op.create_table(
        'user_sessions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('session_token', sa.String(length=255), nullable=False),
        sa.Column('refresh_token', sa.String(length=255), nullable=True),
        sa.Column('device_type', sa.String(length=50), nullable=True),
        sa.Column('device_name', sa.String(length=100), nullable=True),
        sa.Column('browser', sa.String(length=100), nullable=True),
        sa.Column('browser_version', sa.String(length=50), nullable=True),
        sa.Column('operating_system', sa.String(length=100), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_active_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('logged_out_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_token', name='uq_user_sessions_session_token')
    )
    op.create_index(op.f('ix_user_sessions_id'), 'user_sessions', ['id'], unique=False)
    op.create_index('ix_user_sessions_user_id', 'user_sessions', ['user_id'], unique=False)

    op.alter_column('users', 'notification_settings', server_default=None)
    op.alter_column('users', 'preferences', server_default=None)


def downgrade() -> None:
    op.drop_index('ix_user_sessions_user_id', table_name='user_sessions')
    op.drop_index(op.f('ix_user_sessions_id'), table_name='user_sessions')
    op.drop_table('user_sessions')

    op.drop_column('users', 'preferences')
    op.drop_column('users', 'notification_settings')
