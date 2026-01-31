"""add_rewrite_history_tables

Revision ID: a1b2c3d4e5f6
Revises: f1g2h3i4j5k6
Create Date: 2025-10-25 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8h9i0j1k2l3m'
down_revision = 'f1g2h3i4j5k6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建 rewrite_sessions 表
    op.create_table(
        'rewrite_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('original_text', sa.Text(), nullable=False),
        sa.Column('context_before', sa.Text(), nullable=True),
        sa.Column('context_after', sa.Text(), nullable=True),
        sa.Column('mode', sa.String(length=50), nullable=False),
        sa.Column('custom_requirement', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rewrite_sessions_id'), 'rewrite_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_rewrite_sessions_user_id'), 'rewrite_sessions', ['user_id'], unique=False)
    op.create_index(op.f('ix_rewrite_sessions_created_at'), 'rewrite_sessions', ['created_at'], unique=False)

    # 创建 rewrite_results 表
    op.create_table(
        'rewrite_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('rewritten_text', sa.Text(), nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=False),
        sa.Column('elapsed_time', sa.Float(), nullable=False),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('is_selected', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['rewrite_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rewrite_results_id'), 'rewrite_results', ['id'], unique=False)
    op.create_index(op.f('ix_rewrite_results_session_id'), 'rewrite_results', ['session_id'], unique=False)


def downgrade() -> None:
    # 删除 rewrite_results 表
    op.drop_index(op.f('ix_rewrite_results_session_id'), table_name='rewrite_results')
    op.drop_index(op.f('ix_rewrite_results_id'), table_name='rewrite_results')
    op.drop_table('rewrite_results')

    # 删除 rewrite_sessions 表
    op.drop_index(op.f('ix_rewrite_sessions_created_at'), table_name='rewrite_sessions')
    op.drop_index(op.f('ix_rewrite_sessions_user_id'), table_name='rewrite_sessions')
    op.drop_index(op.f('ix_rewrite_sessions_id'), table_name='rewrite_sessions')
    op.drop_table('rewrite_sessions')
