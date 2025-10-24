"""add ai_call_logs table

Revision ID: f1g2h3i4j5k6
Revises: e1f2g3h4i5j6
Create Date: 2025-10-24 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f1g2h3i4j5k6'
down_revision = 'e1f2g3h4i5j6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建 ai_call_logs 表
    op.create_table(
        'ai_call_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('operation_type', sa.String(length=50), nullable=False),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('chapter_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('analysis_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('prompt_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completion_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('prompt_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('completion_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('total_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('is_success', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['analysis_id'], ['novel_analyses.id'], ondelete='SET NULL'),
    )

    # 创建索引
    op.create_index(op.f('ix_ai_call_logs_id'), 'ai_call_logs', ['id'], unique=False)
    op.create_index(op.f('ix_ai_call_logs_user_id'), 'ai_call_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_ai_call_logs_model_name'), 'ai_call_logs', ['model_name'], unique=False)
    op.create_index(op.f('ix_ai_call_logs_operation_type'), 'ai_call_logs', ['operation_type'], unique=False)
    op.create_index(op.f('ix_ai_call_logs_work_id'), 'ai_call_logs', ['work_id'], unique=False)
    op.create_index(op.f('ix_ai_call_logs_chapter_id'), 'ai_call_logs', ['chapter_id'], unique=False)
    op.create_index(op.f('ix_ai_call_logs_analysis_id'), 'ai_call_logs', ['analysis_id'], unique=False)
    op.create_index(op.f('ix_ai_call_logs_created_at'), 'ai_call_logs', ['created_at'], unique=False)

    # 创建复合索引
    op.create_index('ix_ai_logs_user_created', 'ai_call_logs', ['user_id', 'created_at'], unique=False)
    op.create_index('ix_ai_logs_model_created', 'ai_call_logs', ['model_name', 'created_at'], unique=False)
    op.create_index('ix_ai_logs_operation_created', 'ai_call_logs', ['operation_type', 'created_at'], unique=False)
    op.create_index('ix_ai_logs_work_created', 'ai_call_logs', ['work_id', 'created_at'], unique=False)


def downgrade() -> None:
    # 删除复合索引
    op.drop_index('ix_ai_logs_work_created', table_name='ai_call_logs')
    op.drop_index('ix_ai_logs_operation_created', table_name='ai_call_logs')
    op.drop_index('ix_ai_logs_model_created', table_name='ai_call_logs')
    op.drop_index('ix_ai_logs_user_created', table_name='ai_call_logs')

    # 删除单列索引
    op.drop_index(op.f('ix_ai_call_logs_created_at'), table_name='ai_call_logs')
    op.drop_index(op.f('ix_ai_call_logs_analysis_id'), table_name='ai_call_logs')
    op.drop_index(op.f('ix_ai_call_logs_chapter_id'), table_name='ai_call_logs')
    op.drop_index(op.f('ix_ai_call_logs_work_id'), table_name='ai_call_logs')
    op.drop_index(op.f('ix_ai_call_logs_operation_type'), table_name='ai_call_logs')
    op.drop_index(op.f('ix_ai_call_logs_model_name'), table_name='ai_call_logs')
    op.drop_index(op.f('ix_ai_call_logs_user_id'), table_name='ai_call_logs')
    op.drop_index(op.f('ix_ai_call_logs_id'), table_name='ai_call_logs')

    # 删除表
    op.drop_table('ai_call_logs')
